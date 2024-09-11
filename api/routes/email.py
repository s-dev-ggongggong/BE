# File: api/routes/email.py

from flask import Blueprint, request, jsonify
from api.services import email_service
from api.services.training_service import get_random_employees
from api.services.email_service import send_phishing_emails, check_and_set_action_for_email
from models.email import Email

from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import  bad_request, not_found, server_error
from utils.api_error_handlers import api_errorhandler
 
email_bp = Blueprint('email_bp', __name__)

@api_errorhandler(email_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@email_bp.route('/', methods=['GET'])
def get_emails():
    try:
        emails, status = email_service.get_emails()
        return jsonify({"message": "Emails retrieved successfully.", "data": emails}), status
    except Exception as e:
        return jsonify({"error": f"Error while fetching emails: {str(e)}"}), 500

@email_bp.route('/<int:email_id>', methods=['GET'])
def get_email(email_id):
    try:
        email, status = email_service.get_email(email_id)
        if status == 404:
            return jsonify({"error": f"Email with ID {email_id} not found."}), 404
        return jsonify({"message": "Email retrieved successfully.", "data": email}), status
    except Exception as e:
        return jsonify({"error": f"Error while fetching email: {str(e)}"}), 500

@email_bp.route('/', methods=['POST'])
def create_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is empty."}), 400
        email, status = email_service.create_email(data)
        return jsonify({"message": "Email created successfully.", "data": email}), status
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error while creating email: {str(e)}"}), 500

@email_bp.route('/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is empty."}), 400
        email, status = email_service.update_email(email_id, data)
        if status == 404:
            return jsonify({"error": f"Email with ID {email_id} not found."}), 404
        return jsonify({"message": "Email updated successfully.", "data": email}), status

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error while updating email: {str(e)}"}), 500

@email_bp.route('/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    try:
        response, status = email_service.delete_email(email_id)
        if status == 404:
            return jsonify({"error": f"Email with ID {email_id} not found."}), 404
        return jsonify({"message": "Email deleted successfully.", "data": response}), status
    except Exception as e:
        return jsonify({"error": f"Error while deleting email: {str(e)}"}), 500

@email_bp.route('/phishing/log', methods=['POST'])
def generate_phishing_logs():
    try:
        data = request.get_json()
        if not data:
            return bad_request("Request body is empty.")
        logs, status = email_service.generate_phishing_logs(data)
        return jsonify({"message": "Phishing logs generated successfully.", "data": logs}), status
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error while generating phishing logs: {str(e)}"}), 500


@email_bp.route('/phishing/<int:training_id>', methods=['POST'])
def send_emails(training_id):
    try:
        employee_list = request.json.get('employees', [])
        if not employee_list:
            return {"error": "Employee list is missing."}, 400

        # Call the send_phishing_emails function
        sent_emails = send_phishing_emails(training_id, employee_list)
        return jsonify({"message": "Phishing emails sent", "data": sent_emails}), 200
    except Exception as e:
        return jsonify({"error": f"Error sending phishing emails: {str(e)}"}), 500
    

@email_bp.route('/action/<int:email_id>', methods=['GET'])
def check_email_action(email_id):
    try:
        email = Email.query.get(email_id)
        if not email:
            return {"error": "Email not found"}, 404

        action = check_and_set_action_for_email(email)
        if action:
            return jsonify({"message": f"Action '{action}' set for email"}), 200
        return jsonify({"message": "No action needed for the email"}), 200
    except Exception as e:
        return jsonify({"error": f"Error checking email action: {str(e)}"}), 500