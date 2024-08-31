from flask import Flask, request, jsonify, make_response
from extensions import db,ma
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config

def create_app():
    app= Flask(__name__)
    #set configs
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)


 
    SWAGGER_BLUEPRINT=get_swaggerui_blueprint(
        Config.SWAGGER_URL,
        Config.API_URL,
        config=Config.SWAGGER_CONFIG
    )

    app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=Config.SWAGGER_URL )



    with app.app_context():
        # import Model
        from model import models
        # import routes
        db.create_all()

        from route.routes import routes
        app.register_blueprint(routes)
    return app

# if __name__ == '__main__':
#     app=create_app()
#     print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
#     app.run(debug=True)