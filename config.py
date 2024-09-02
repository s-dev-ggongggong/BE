import os
from sqlalchemy import create_engine
class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_NOTIFICATIONS',False)
    SWAGGER_URL = '/swagger'
    DEBUG=True
    ENGINE=create_engine(SQLALCHEMY_DATABASE_URI)
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
    IMAP_SERVER = '10.0.10.162'
    USERNAME = 'test4'
    PASSWORD = 'igloo1234'