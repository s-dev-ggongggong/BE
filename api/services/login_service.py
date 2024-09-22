from models.employee import Employee  # Employee 모델 임포트
from extensions import db  # DB 세션 임포트
from flask_jwt_extended import create_access_token
from utils.http_status_handler import bad_request, unauthorized

# 로그인 로직 처리 함수
def login_service(data):
    try:
        # 입력된 JSON 데이터에서 admin_id와 admin_pw 추출
        admin_id = data.get('admin_id')
        admin_pw = data.get('admin_pw')

        # 입력값 유효성 검증
        if not admin_id or not admin_pw:
            return bad_request("Admin ID and password required")

        # DB에서 admin_id로 관리자 정보 조회
        employee = db.session.query(Employee).filter_by(admin_id=admin_id).first()

        # 관리자가 존재하지 않거나 비밀번호가 일치하지 않는 경우
        if not employee or employee.admin_pw != admin_pw:
            return unauthorized("Invalid admin ID or password")

        # JWT 토큰 생성
        access_token = create_access_token(identity=admin_id)
        return {"access_token": access_token}, 200

    except Exception as e:
        return {"error": str(e)}, 500  # 예외 처리
