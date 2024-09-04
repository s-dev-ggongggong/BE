import os,sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate, upgrade, init, migrate as migrate_command
from sqlalchemy import inspect
from config import Config
from extensions import db, ma, migrate, init_extensions
from werkzeug.exceptions import HTTPException
from api.routes import routes
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @routes.app_errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": str(e)}), e.code
        if isinstance(e,ValidationError):
            return jsonify({"message": "Validation error", "errors": e.messages}), 400
        if isinstance(e, SQLAlchemyError):
            return jsonify({"error": "Database error", "details": str(e)}), 500
        # Handle all other exceptions
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Database URI: {app.config.get ('SQLALCHEMY_DATABASE_URI','Not set')}")

    init_extensions(app)

    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        Config.SWAGGER_URL,
        Config.API_URL,
        config=Config.SWAGGER_CONFIG
    )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=Config.SWAGGER_URL)

    register_error_handlers(app)
    
    with app.app_context():
        from models import department, employee, role, email, dashboard, training, models, schemas
         
        from api.routes import routes
        app.register_blueprint(routes)

        print("check db connection :")
        try:
            db.engine.connect()
            print("db connect success")
        except Exception as e:
            print(f'Database connection failed :{str(e)}')

        print("Existing tables ", inspect(db.engine).get_table_names())

        if not os.path.exists('migrations'):
            print("Initializing migrate")
            init()

            print("Running migrations")
            migrate_command()

            print("upgrading database!!!!!!!")
            upgrade()

            print("final table list:", inspect(db.engine).get_table_names())

    return app

def init_db(app):
    with app.app_context():
        if not os.path.exists('migrations'):
            print("Initializing migrate")
            from flask_migrate import init, migrate as migrate_command, upgrade
            init()
            print("Running migrations")
            migrate_command()
            print("upgrading database!!!!!!!")
            upgrade()
            print("final table list:", inspect(db.engine).get_table_names())