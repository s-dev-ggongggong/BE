from flask import Blueprint, request, jsonify
from api.services import department_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import server_error

department_bp = Blueprint('departments', __name__)

@api_errorhandler(department_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500


@department_bp.route('/', methods=['GET'])
def get_all_departments_route():
    try:
        response, status = department_service.get_all_departments()
        return jsonify({"data": response, "message": "모든 부서 정보를 성공적으로 조회했습니다."}), status
    except Exception as e:
        return server_error(f"Error fetching departments: {str(e)}")

@department_bp.route('/<int:id>', methods=['GET'])
def get_department_route(id):
    try:
        response, status = department_service.get_department_by_id(id)
        if status == 404:
            return jsonify({"error": f"Department with ID {id} not found"}), 404
        return jsonify({"data": response, "message": f"Department ID {id} fetched successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error fetching department: {str(e)}"}), 500

@department_bp.route('/', methods=['POST'])
def create_department_route():
    data = request.get_json()
    if not data:
        return jsonify({"error":"No data provided"}),400
    response, status = department_service.create_new_department(data)
    if status == 201:
        return jsonify({"message": "새로운 부서가 성공적으로 생성되었습니다.", "data": response}), status
    else:
        return jsonify({"message": response}), status

@department_bp.route('/<int:id>', methods=['PUT'])
def update_department_route(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}),400
    response, status = department_service.update_department(id, data)
    if status == 404:
        return jsonify({"error": f"Department with ID {id} not found"}), 404
    return jsonify({"message": response, "message": f"Department ID {id} updated successfully"}), status

@department_bp.route('/<int:id>', methods=['DELETE'])
def delete_department(id):
    response, status = department_service.delete_department(id)
    if status != 200:
        return jsonify(response), status
    return jsonify({"data": response, "message": f"Department ID {id} deleted successfully"}), status


