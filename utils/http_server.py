import sys
import os
import base64
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer  # http.server 모듈을 임포트

# 현재 디렉터리의 상위 디렉터리를 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from models.event_log import EventLog

# Flask 애플리케이션 생성
app = create_app()

# HTTP 서버 요청 처리기
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/click':
            query_params = parse_qs(parsed_url.query)
            user_param = query_params.get('user', [None])[0]

            if user_param:
                try:
                    decoded_user_data = base64.urlsafe_b64decode(user_param).decode()
                    user_data = json.loads(decoded_user_data)

                    # Flask 애플리케이션 컨텍스트 내에서 DB 작업 수행
                    with app.app_context():
                        self.log_event(user_data)

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Phishing link clicked! Thank you.")
                except Exception as e:
                    self.send_response(400)
                    self.end_headers()
                    error_message = f"Invalid user data: {str(e)}"
                    self.wfile.write(error_message.encode())
                    print(error_message)
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing user parameter.")
        else:
            self.send_response(404)
            self.end_headers()
    

    # 유저 클릭 이벤트를 event_logs 테이블에 기록하는 함수
    def log_event(self, user_data):
        try:
            new_event = EventLog(
                action='clicked_link',
                timestamp=datetime.utcnow() + timedelta(hours=9),  # 한국 시간으로 변경
                employee_id=user_data['id'],
                department_id=user_data['department_name'],  # department_name을 department_id로 가정
                message=f"User {user_data['name']} clicked phishing link"
            )

            new_event.set_data({
                "user_data": user_data,
                "action": "clicked_link"
            })

            db.session.add(new_event)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

# HTTP 서버 실행 함수
def run_server(port=7777):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

# 서버 실행
if __name__ == "__main__":
    run_server()
