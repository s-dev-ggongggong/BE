import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    DEBUG = os.getenv('FLASK_DEBUG', True)
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    STRICT_SLASHES = False
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    USERNAME = os.getenv('IMAP_USERNAME')
    PASSWORD = os.getenv('IMAP_PASSWORD')   