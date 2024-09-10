# File: api/routes/employee.py

from flask import Blueprint, request, jsonify
from api.services import employee_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import handle_response, not_found, bad_request, server_error

employee_bp = Blueprint('employee_bp', __name__)

@api_errorhandler(employee_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@employee_bp.route('/', methods=['GET'])
def get_users():
    users, status = employee_service.get_all_users()
    return handle_response(status, data=users, message="Employees retrieved successfully")

@employee_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user, status = employee_service.get_user_by_id(id)
    if status == 404:
        return not_found(f"Employee with ID {id} not found")
    return handle_response(status, data=user, message="Employee retrieved successfully")

@employee_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return bad_request("Request body is empty")
    user, status = employee_service.create_user(data)
    return handle_response(status, data=user, message="Employee created successfully")

@employee_bp.route('/with-training', methods=['GET'])
def get_users_with_trainings():
    users, status = employee_service.get_users_with_trainings()
    return handle_response(status, data=users, message="Employees with trainings retrieved successfully")
