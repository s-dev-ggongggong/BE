from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.services.login_service import login_service  # login_service 임포트

# Blueprint 생성
login_bp = Blueprint('login_bp', __name__)

# 로그인 엔드포인트
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        # 요청으로부터 데이터 받아오기
        data = request.get_json()

        # 서비스 호출 및 응답 반환
        response, status = login_service(data)
        return jsonify(response), status
    except:
        return jsonify({"msg": "Invalid input format"}), 400

# 권한 확인 함수 (admin_id로 직원 조회)
@jwt_required()
def get_employee_user():
    current_user_admin_id = get_jwt_identity()  # 토큰에서 현재 사용자 admin_id를 가져옴
    employee = db.session.query(Employee).filter_by(admin_id=current_user_admin_id).first()  # admin_id로 직원 조회
    if not employee:
        return None
    return employee
