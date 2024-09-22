import base64
import json
from models.employee import Employee
from models.event_log import EventLog
from utils.http_status_handler import not_found
from datetime import datetime,timedelta

# 피싱 링크 생성 서비스
def generate_phishing_link(user_id, db_session, training_id):
    # 데이터베이스에서 유저 정보 조회
    user = db_session.query(Employee).filter_by(id=user_id).first()

    if user:
        # 유저 정보를 딕셔너리로 생성
        user_data = {
            "id": user.id,
            "name": user.name,
            "role_name": user.role_name,
            "department_name": user.department_name
        }

        # 유저 정보를 JSON으로 변환 후 Base64로 인코딩
        encoded_user_data = base64.urlsafe_b64encode(json.dumps(user_data).encode()).decode()

        # 인코딩된 유저 데이터 출력
        
        print(f"Encoded user data: {encoded_user_data}")

         # 피싱 링크 생성
        server_url = "http://127.0.0.1:7777"
        phishing_link = f"{server_url}/click?user={encoded_user_data}"

        # 한국 시간으로 변경
        timestamp_kst = datetime.utcnow() + timedelta(hours=9)

        # 이벤트 로그 기록
        event_log = EventLog(
            action='phishing_link_click',
            timestamp=timestamp_kst,
            training_id=training_id,
            message=f"Phishing link generated for user {user.name}",
            employee_id=user.id,
            department_id=None
        )

        # 추가 데이터를 JSON으로 저장
        event_log.set_data({
            "user_data": user_data,
            "phishing_link": phishing_link
        })

        # 로그 기록을 데이터베이스에 저장
        db_session.add(event_log)
        db_session.commit()

        return phishing_link, 200

    return not_found(f"User with ID {user_id} not found")

