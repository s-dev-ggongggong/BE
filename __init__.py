from flask import Flask, request, jsonify
from extensions import db,ma
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from routes.routes import routes

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
     
        
        db.drop_all()        
        db.create_all()

        app.register_blueprint(routes)
        
    return app
 