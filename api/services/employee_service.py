# File: api/services/employee_service.py

from models.employee import Employee
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import employee_schema
from utils.http_status_handler import handle_response ,server_error,unauthorized
from flask_jwt_extended import create_access_token
 
from utils.string_utils import convert_dict_keys_to_snake_case

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


def admin_login(admin_id, admin_pw):
    admin_id = convert_dict_keys_to_snake_case({"adminId": admin_id})["admin_id"]
    admin_pw = convert_dict_keys_to_snake_case({"adminPw": admin_pw})["admin_pw"]

    if admin_id == 'admin' and admin_pw == 'admin1234':
        access_token = create_access_token(identity=admin_id)
        admin_info = {
            "id": 1,
            "name": 'ADMIN',
            "email": 'admin@ip-10-0-10-162.ap-northeast-2.compute.internal',
            "department_name": '정보기술부',
            "role_name": 'IT 관리자',
            "admin_id": 'admin',
        }
        return {
            "status": 200, 
            "data": {
                "access_token": access_token,
                "admin_info": admin_info
            }, 
            "message": "로그인 성공"
        }, 200
    return {"status": 401, "message": "잘못된 관리자 정보"}, 401

    

       
        

   