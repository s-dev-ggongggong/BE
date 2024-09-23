import sys
import os
import base64
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# 현재 디렉터리의 상위 디렉터리를 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from api.services.phishing_service import PhishingEvent

# Flask 애플리케이션 생성
app = create_app()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/click':
            query_params = parse_qs(parsed_url.query)
            user_param = query_params.get('user', [None])[0]

            if user_param:
                try:
                    # base64 디코딩하여 유저 데이터 추출
                    decoded_user_data = base64.urlsafe_b64decode(user_param).decode()
                    user_data = json.loads(decoded_user_data)

                    # Flask 애플리케이션 컨텍스트 내에서 DB 작업 수행
                    with app.app_context():
                        phishing_event = PhishingEvent(db.session)
                        phishing_event.log_click_event(user_data)

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Phishing link clicked! Thank you.")
                except Exception as e:
                    self.send_response(400)
                    self.end_headers()
                    error_message = f"Invalid user data: {str(e)}"
                    self.wfile.write(error_message.encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing user parameter.")
        else:
            self.send_response(404)
            self.end_headers()

# HTTP 서버 실행 함수
def run_server(port=7777):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
