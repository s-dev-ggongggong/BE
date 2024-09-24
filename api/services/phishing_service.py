import base64
import json
from models.employee import Employee
from models.user_event_log import UserEventLog
from utils.http_status_handler import not_found
from datetime import datetime, timedelta

class PhishingEvent:
    def __init__(self, db_session):
        self.db_session = db_session

    def generate_phishing_link(self, user_id, training_id, email_id):
        """
        피싱 링크 생성 후, 결과를 반환합니다. (user_event_log에 기록하지 않음)
        """
        # 유저 정보 조회
        user = self.db_session.query(Employee).filter_by(id=user_id).first()

        if user:
            # 유저 데이터를 딕셔너리로 변환
            user_data = {
                "id": user.id,
                "name": user.name,
                "department_name": user.department_name,
                "email_id": email_id  # email_id 추가
            }

            # 유저 정보를 JSON으로 변환 후 Base64로 인코딩
            encoded_user_data = base64.urlsafe_b64encode(json.dumps(user_data).encode()).decode()

            # 피싱 링크 생성
            server_url = "http://127.0.0.1:7777"
            phishing_link = f"{server_url}/click?user={encoded_user_data}"

            return phishing_link, 200

        return not_found(f"User with ID {user_id} not found")


    def log_click_event(self, user_data):
        """
        피싱 링크 클릭 여부를 user_event_log 테이블에 기록합니다.
        """
        # 현재 시간을 한국 표준시(KST)로 설정
        timestamp_kst = datetime.utcnow() + timedelta(hours=9)

        log_message = f"{user_data['department_name']} 부서의 {user_data['name']}가 피싱 링크를 클릭했습니다."

        # user_event_log에 클릭 여부 기록
        event_log = UserEventLog(
            user_id=user_data['id'],
            user_name=user_data['name'],
            department_name=user_data['department_name'],
            email_id=user_data['email_id'],  # email_id는 employee 테이블의 email 필드 값
            event_type="link_clicked",
            timestamp=timestamp_kst,
            data=json.dumps({"action": "clicked_link"})
        )

        # 로그를 데이터베이스에 저장
        self.db_session.add(event_log)
        self.db_session.commit()
