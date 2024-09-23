from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, ma, migrate, jwt  
from config import Config
from api import init_routes, api_bp
from api.routes.login import login_bp
from api.routes.phishing import phishing_bp 
import os  

def setup_swagger(app, config):
    swaggerui_blueprint = get_swaggerui_blueprint(
        config.SWAGGER_URL,
        config.API_URL,
        config=config.SWAGGER_CONFIG
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=config.SWAGGER_URL)

    @app.route(config.API_URL)
    def send_swagger_json():
        return send_from_directory('static', 'swagger.json')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # JWT 초기화 추가

    # Register API blueprint
    app.register_blueprint(api_bp)
    app.register_blueprint(login_bp, url_prefix='/')  # login_bp를 최상위 경로에 등록
    app.register_blueprint(phishing_bp, url_prefix='/')

    setup_swagger(app, config_class)

    @app.route('/')
    def root():
        return "Welcome to the Email application"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8000)  # 하나의 run()만 사용
