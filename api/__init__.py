# File: api/__init__.py
from flask import Blueprint, redirect, jsonify

api_bp = Blueprint('api', __name__)

# Import routes after creating the blueprint to avoid circular imports

from api.routes.employee import  employee_bp
from api.routes.email import  email_bp
from api.routes.training import  training_bp
from api.routes.department import  department_bp
from api.routes.role import  role_bp
from api.routes.event_log import  event_log_bp
from api.routes.complete_training import complete_bp 
 
# def index():
#     return redirect('/swagger')

def init_routes():
    routes = [
 
        (employee_bp, '/employee'),
        (email_bp, '/email'),
        (training_bp, '/training'),
        (department_bp, '/department'),
        (role_bp, '/role'),
        (event_log_bp, '/eventlog'),
        (complete_bp, '/training-c')
 
    ]

    for route_blueprint, url_prefix in routes:
        api_bp.register_blueprint(route_blueprint, url_prefix=url_prefix)

# Initialize routes
init_routes()