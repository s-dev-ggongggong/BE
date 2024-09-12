# File: api/routes/email.py

from flask import Blueprint, request, jsonify
from api.services import email_service
from api.services.training_service import get_random_employees
from api.services.email_service import send_phishing_emails, check_and_set_action_for_email
from models.email import Email
from models.schemas import emails_schema
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import  bad_request, not_found, server_error
from utils.api_error_handlers import api_errorhandler
 
email_bp = Blueprint('email_bp', __name__)

@api_errorhandler(email_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@email_bp.route('/', methods=['GET'])
def get_emails():
    response = email_service.get_emails()
    return jsonify(response), response['status_code']
    

@email_bp.route('/<int:email_id>', methods=['GET'])
def get_email(email_id):
    response = email_service.get_email(email_id)
    return jsonify(response), response['status_code']

@email_bp.route('/', methods=['POST'])
def create_email():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is empty."}), 400
    response = email_service.create_email(data)
    return jsonify(response), response['status_code']

@email_bp.route('/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is empty."}), 400
    response = email_service.update_email(email_id, data)
    return jsonify(response), response['status_code']

@email_bp.route('/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    response = email_service.delete_email(email_id)
    return jsonify(response), response['status_code']

@email_bp.route('/phishing/log', methods=['POST'])
def generate_phishing_logs():
    data = request.get_json()
    response = email_service.generate_phishing_logs(data)
    return jsonify(response), response['status_code']



@email_bp.route('/phishing/<int:training_id>', methods=['POST'])
def send_emails(training_id):
    employee_list = request.json.get('employees', [])
    if not employee_list:
        return jsonify({"error": "Employee list is missing."}), 400
    response = email_service.send_phishing_emails(training_id, employee_list)
    return jsonify(response), response['status_code']

@email_bp.route('/action/<int:email_id>', methods=['GET'])
def check_email_action(email_id):
    response = email_service.check_and_set_action_for_email(email_id)
    return jsonify(response), response['status_code']