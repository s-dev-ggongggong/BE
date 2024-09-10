# File: api/routes/email.py

from flask import Blueprint, request, jsonify
from utils.api_error_handlers import api_errorhandler
from api.services import email_service
from utils.http_status_handler import handle_response, bad_request, not_found, server_error

email_bp = Blueprint('email_bp', __name__)

@api_errorhandler(email_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@email_bp.route('/', methods=['GET'])
def get_emails():
    try:
        emails, status = email_service.get_emails()
        return handle_response(status, data=emails, message="Emails retrieved successfully.")
    except Exception as e:
        return server_error(f"Error while fetching emails: {str(e)}")

@email_bp.route('/<int:email_id>', methods=['GET'])
def get_email(email_id):
    try:
        email, status = email_service.get_email(email_id)
        if status == 404:
            return not_found(f"Email with ID {email_id} not found.")
        return handle_response(status, data=email, message="Email retrieved successfully.")
    except Exception as e:
        return server_error(f"Error while fetching email: {str(e)}")

@email_bp.route('/', methods=['POST'])
def create_email():
    try:
        data = request.get_json()
        if not data:
            return bad_request("Request body is empty.")
        email, status = email_service.create_email(data)
        return handle_response(status, data=email, message="Email created successfully.")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error while creating email: {str(e)}")

@email_bp.route('/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    try:
        data = request.get_json()
        if not data:
            return bad_request("Request body is empty.")
        email, status = email_service.update_email(email_id, data)
        if status == 404:
            return not_found(f"Email with ID {email_id} not found.")
        return handle_response(status, data=email, message="Email updated successfully.")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error while updating email: {str(e)}")

@email_bp.route('/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    try:
        response, status = email_service.delete_email(email_id)
        if status == 404:
            return not_found(f"Email with ID {email_id} not found.")
        return handle_response(status, data=response, message="Email deleted successfully.")
    except Exception as e:
        return server_error(f"Error while deleting email: {str(e)}")

@email_bp.route('/phishing', methods=['POST'])
def generate_phishing_logs():
    try:
        data = request.get_json()
        if not data:
            return bad_request("Request body is empty.")
        logs, status = email_service.generate_phishing_logs(data)
        return handle_response(status, data=logs, message="Phishing logs generated successfully.")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error while generating phishing logs: {str(e)}")
