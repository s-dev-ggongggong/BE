import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate, upgrade, init, migrate as migrate_command
from sqlalchemy import inspect

from config import Config
from extensions import db, ma, migrate, init_extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    init_extensions(app)

    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        Config.SWAGGER_URL,
        Config.API_URL,
        config=Config.SWAGGER_CONFIG
    )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=Config.SWAGGER_URL)

    with app.app_context():
        from models import user, email, dashboard, training, models, schemas
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