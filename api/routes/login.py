from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.employee import Employee  # 올바르게 Employee 모델을 임포트
from extensions import db  # DB 세션 임포트

# Blueprint 생성
login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    try:
        # admin_id와 admin_pw를 JSON 형식으로 받아오기
        data = request.get_json()
        admin_id = data.get('admin_id')
        admin_pw = data.get('admin_pw')
    except:
        return jsonify({"msg": "Invalid input format"}), 400

    # 입력 값 확인
    if not admin_id or not admin_pw:
        return jsonify({"msg": "Admin ID and password required"}), 400

    # DB에서 admin_id로 관리자 찾기
    employee = db.session.query(Employee).filter_by(admin_id=admin_id).first()
    if not employee or employee.admin_pw != admin_pw:
        return jsonify({"msg": "Invalid admin ID or password"}), 401

    # jwt 토큰 생성
    access_token = create_access_token(identity=admin_id)
    return jsonify(access_token=access_token), 200


# 권한 확인 함수 (admin_id로 직원 조회)
@jwt_required()
def get_employee_user():
    current_user_admin_id = get_jwt_identity()  # 토큰에서 현재 사용자 admin_id를 가져옴
    employee = db.session.query(Employee).filter_by(admin_id=current_user_admin_id).first()  # admin_id로 직원 조회
    if not employee:
        return None
    return employee
