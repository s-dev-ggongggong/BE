from flask import jsonify, request,Blueprint
from model.models import DashboardItem, dashboard_items_schema,User, user_schema,users_schema,Email,emails_schema
from extensions import ma, db

routes=Blueprint('routes',__name__)

@routes.route('/')
def home():
    return "Welcom Email Test"

@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@routes.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@routes.route('/user',methods=['POST'])
def add_user():
    username=request.json['username']
    email = request.json['email']
    password=request.json['password']

    new_user =User(username=username,email=email,password_hash=password)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@routes.route('/dashboard', methods=['GET'])
def get_dashboard():
    items = DashboardItem.query.all()
    return dashboard_items_schema.jsonify(items)

@routes.route('/emails', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    return emails_schema.jsonify(emails)