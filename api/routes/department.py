from flask import Blueprint, request, jsonify
from api.services.department_service import (
    get_all_departments, create_new_department, get_department_by_id, 
    update_department, delete_department, get_departments_with_roles
)

department_bp = Blueprint('departments', __name__)

@department_bp.route('/', methods=['GET'])
def get_all_departments_route():
    result, status = get_all_departments()
    return jsonify({"message": "모든 부서 정보를 성공적으로 조회했습니다.", "data": result}), status

@department_bp.route('/<int:id>', methods=['GET'])
def get_department_route(id):
    result, status = get_department_by_id(id)
    if status == 200:
        return jsonify({"message": f"ID {id} 부서 정보를 성공적으로 조회했습니다.", "data": result}), status
    else:
        return jsonify({"message": result}), status

@department_bp.route('/', methods=['POST'])
def create_department_route():
    data = request.get_json()
    result, status = create_new_department(data)
    if status == 201:
        return jsonify({"message": "새로운 부서가 성공적으로 생성되었습니다.", "data": result}), status
    else:
        return jsonify({"message": result}), status

@department_bp.route('/<int:id>', methods=['PUT'])
def update_department_route(id):
    data = request.get_json()
    result, status = update_department(id, data)
    if status == 200:
        return jsonify({"message": f"ID {id} 부서 정보가 성공적으로 업데이트되었습니다.", "data": result}), status
    else:
        return jsonify({"message": result}), status

@department_bp.route('/<int:id>', methods=['DELETE'])
def delete_department_route(id):
    result, status = delete_department(id)
    return jsonify({"message": result}), status

@department_bp.route('/roles', methods=['GET'])
def get_departments_roles_route():
    result, status = get_departments_with_roles()
    if status == 200:
        return jsonify({"message": "부서와 역할 정보를 성공적으로 조회했습니다.", "data": result}), status
    else:
        return jsonify({"message": result}), status