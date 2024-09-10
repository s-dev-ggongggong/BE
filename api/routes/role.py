from flask import Blueprint, request, jsonify
from api.services import role_service

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/', methods=['GET'])
def get_all_roles():
    result, status_code = role_service.get_all_roles()
    return jsonify({"message": "역할 목록을 성공적으로 가져왔습니다.", "data": result}), status_code

@role_bp.route('/<int:id>', methods=['GET'])
def get_role(id):
    result, status_code = role_service.get_role_by_id(id)
    if status_code == 200:
        return jsonify({"message": f"ID가 {id}인 역할을 성공적으로 가져왔습니다.", "data": result}), status_code
    else:
        return jsonify({"message": result}), status_code

@role_bp.route('/', methods=['POST'])
def create_role():
    data = request.get_json()
    result, status_code = role_service.create_new_role(data)
    if status_code == 201:
        return jsonify({"message": "새로운 역할이 성공적으로 생성되었습니다.", "data": result}), status_code
    else:
        return jsonify({"message": result}), status_code

@role_bp.route('/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.get_json()
    result, status_code = role_service.update_role(id, data)
    if status_code == 200:
        return jsonify({"message": f"ID가 {id}인 역할이 성공적으로 업데이트되었습니다.", "data": result}), status_code
    else:
        return jsonify({"message": result}), status_code

@role_bp.route('/<int:id>', methods=['DELETE'])
def delete_role(id):
    result, status_code = role_service.delete_role(id)
    return jsonify({"message": result}), status_code