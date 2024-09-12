# File: api/services/employee_service.py

from models.employee import Employee
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import employee_schema
from utils.http_status_handler import handle_response ,server_error
def get_all_users():
    try:
        users = Employee.query.all()
        result = [
            {"id": user.id, "name": user.name, "email": user.email, "department_name": user.department_name, "role_name": user.role_name}
            for user in users
        ]
        return result, 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def get_user_by_id(user_id):
    try:
        user = Employee.query.get_or_404(user_id)
        return {
            "id": user.id, "name": user.name, "email": user.email, "department_name": user.department_name, "role_name": user.role_name
        }, 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def create_user(data):
    try:
        new_user = Employee(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # Consider hashing this
            department_name=data['department_name'],
            role_name=data['role_name']
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Employee created", "user": {"id": new_user.id, "name": new_user.name}}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_users_with_trainings():
    try:
        users = Employee.query.all()
        result = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "trainings": [{"id": training.id, "name": training.training_name} for training in user.trainings]
            }
            for user in users
        ]
        return result, 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500
def create_employee(data):
    try:
        # 비밀번호를 포함한 데이터 처리
        employee = Employee(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # 비밀번호 삽입
            department_name=data['department_name'],
            role_name=data['role_name']
        )
        db.session.add(employee)
        db.session.commit()
        return handle_response(201, data=employee_schema.dump(employee), message="Employee created successfully.")
    except Exception as e:
        return server_error(f"Error creating employee: {str(e)}")
def get_admin_info():
    try:
        admin_user = Employee.query.filter_by(name="admin").first()
        
        if admin_user:
            return {
                "id": admin_user.id,
                "name": admin_user.name,
                "email": admin_user.email,
                "department_name": admin_user.department_name,
                "role_name": admin_user.role_name,
                "admin_id": admin_user.admin_id,
                "admin_pw": admin_user.admin_pw  # Be cautious about returning this
            }, 200
        else:
            return {"error": "Admin user not found"}, 404
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500