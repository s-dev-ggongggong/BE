# File: api/routes/employee.py

from flask import Blueprint, request, jsonify
from api.services import employee_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import handle_response, not_found, bad_request, server_error
from flask_jwt_extended import  get_jwt_identity, jwt_required
from utils.string_utils import convert_dict_keys_to_snake_case

employee_bp = Blueprint('employee_bp', __name__)

@api_errorhandler(employee_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@employee_bp.route('/', methods=['GET'])
def get_employees():
    department_id = request.args.get('department_id', type=int)
    role_id = request.args.get('role_id', type=int)
    employee_id = request.args.get('employee_id', type=int)
    search = request.args.get('search')

    result, status_code = employee_service.get_users(
        department_id=department_id,
        role_id=role_id,
        employee_id=employee_id,
        search=search
    )

    return jsonify(result), status_code
@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "해당 필드를 다 기입하세요"}), 400
    response, status_code = employee_service.create_user(data)
    return jsonify(response), status_code

@employee_bp.route('/with-training', methods=['GET'])
def get_users_with_trainings():
    users, status = employee_service.get_users_with_trainings()
    return handle_response(status, data=users, message="Employees with trainings retrieved successfully")
# employee.py




@employee_bp.route('/admin', methods=['POST'])
def admin_login_route():
    data = convert_dict_keys_to_snake_case(request.json)
    login_result, status_code = employee_service.admin_login(data.get('admin_id'), data.get('admin_pw'))
    return jsonify(login_result), status_code