import os

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db', 'e_sol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_NOTIFICATIONS',False)
    SWAGGER_URL = '/swagger'
    DEBUG=True
    API_URL = '/static/swagger.json'
    SWAGGER_CONFIG = {
        'app_name': "Email Test Server"
    }
