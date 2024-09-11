from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.employee import Employee  # 올바르게 Employee 모델을 임포트
from extensions import db  # DB 세션 임포트

# Blueprint 생성
login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    try:
        # name과 password를 JSON 형식으로 받아오기
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')
    except:
        return jsonify({"msg": "Invalid input format"}), 400

    # 입력 값 확인
    if not name or not password:
        return jsonify({"msg": "Name and password required"}), 400

    # DB에서 name으로 관리자 찾기
    employee = db.session.query(Employee).filter_by(name=name).first()
    if not employee or employee.password != password:
        return jsonify({"msg": "Invalid name or password"}), 401

    # jwt 토큰 생성
    access_token = create_access_token(identity=name)
    return jsonify(access_token=access_token), 200


# 권한 확인 함수 (name으로 직원 조회)
@jwt_required()
def get_employee_user():
    current_user_name = get_jwt_identity()  # 토큰에서 현재 사용자 이름을 가져옴
    employee = db.session.query(Employee).filter_by(name=current_user_name).first()  # name으로 직원 조회
    if not employee:
        return None
    return employee
