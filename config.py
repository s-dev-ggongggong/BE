import os
import secrets
from sqlalchemy import create_engine

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # 데이터베이스 URI 설정
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ['true', '1', 't']
    
    # Swagger 설정
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
    
    # JWT 설정
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))  # 환경 변수에서 가져오고 없으면 랜덤값

    # 기타 설정
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
    
    # 이메일 서버 설정
    IMAP_SERVER = os.getenv('IMAP_SERVER', '10.0.10.162')
    USERNAME = os.getenv('EMAIL_USERNAME', 'test4')  # 민감한 정보는 환경 변수에서 가져오는 것이 바람직
    PASSWORD = os.getenv('EMAIL_PASSWORD', 'igloo1234')  # 민감한 정보는 환경 변수에서 관리하는 것이 좋음
