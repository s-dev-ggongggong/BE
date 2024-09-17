from flask import Flask, send_from_directory ,jsonify,request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_cors import CORS
import os
from api import init_routes ,api_bp
from models.training import Training
from dotenv import load_dotenv 
from extensions import db, ma, migrate
from config import Config
from flask_jwt_extended import JWTManager


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
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') # 안전한 비밀키로 변경
    jwt = JWTManager(app)

    CORS(app, resources={r"/*": {"origins": "*"}}) 

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
 
    
    # Register API blueprint
    app.register_blueprint(api_bp)

    setup_swagger(app, config_class)


    @app.route('/training/<int:id>', methods=['OPTIONS'])
    def options(id):
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response

    
    @app.route('/')
    def root():
        return "Welcome to the Email application"

    return app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)

