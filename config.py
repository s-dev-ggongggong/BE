import os,sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from dotenv import load_dotenv
import secrets


from sqlalchemy import create_engine

load_dotenv()
class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_NOTIFICATIONS',False)
    DEBUG=os.getenv('FLASK_DEBUG',True)
    
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    USERNAME = os.getenv('IMAP_USERNAME')
    PASSWORD = os.getenv('IMAP_PASSWORD')
    # 환경 변수에 SECRET_KEY가 없을 경우 secrets 모듈로 랜덤하게 생성
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))  # 16 바이트 길이의 비밀 키 생성