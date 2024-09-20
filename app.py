# Standard Libraries
import os
from dotenv import load_dotenv

# Third-Party Libraries
from flask import Flask, send_from_directory, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Local Modules
from api import init_routes, api_bp
from extensions import db, ma, migrate
from config import Config
from utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

# Set up application logger
logger = setup_logger(__name__)

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
    app.url_map.strict_slashes = app.config['STRICT_SLASHES']
    jwt = JWTManager(app)

    CORS(app, resources={r"/*":  {"origins": "*", "allow_headers": "Content-Type", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}}) 

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register API blueprint
    app.register_blueprint(api_bp)

    # Setup Swagger UI
    setup_swagger(app, config_class)


    @app.route('/')
    def root():
        return "Welcome to the Email application"

    with app.app_context():
        logger.info("Application has started successfully.")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
