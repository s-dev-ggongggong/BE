import os
from sqlalchemy import create_engine

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # 데이터베이스 URI 설정
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_NOTIFICATIONS', False)
    
    # Swagger 설정
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
    
    # JWT 설정 추가
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))  # JWT 토큰에 사용할 비밀키 설정

    # 기타 설정
    DEBUG = True
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
    IMAP_SERVER = '10.0.10.162'
    USERNAME = 'test4'
    PASSWORD = 'igloo1234'
