# File: api/services/employee_service.py

from marshmallow import ValidationError
from models.department import Department
from models.employee import Employee
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import employee_schema
from utils.http_status_handler import handle_response ,server_error,unauthorized
from flask_jwt_extended import create_access_token
 
from utils.string_utils import convert_dict_keys_to_snake_case

# services/employee_service.py
def get_employees_by_filters(role_name=None, department_filters=None):
  query = Employee.query
  if role_name:
        query = query.filter(Employee.role_name == role_name)
  if department_filters:
    query = query.join(Employee.department).filter(*department_filters)
  employees = query.all()


def get_users(department_id=None, role_id=None, employee_id=None, search=None):
    try:
        query = Employee.query

        if employee_id:
            query = query.filter_by(id=employee_id)
        if department_id:
            query = query.filter_by(department_id=department_id)
        if role_id:
            query = query.filter_by(role_id=role_id)
        if search:
            query = query.filter(Employee.name.ilike(f'%{search}%'))

        employees = query.all()

        if not employees:
            return {"message": "직원을 찾을 수 없습니다."}, 404

        result = [
            {
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "department_name": emp.department_name,
                "role_name": emp.role_name
            }
            for emp in employees
        ]

        return result, 200
    except Exception as e:
        return {"error": f"사용자 조회 중 오류 발생: {str(e)}"}, 500


    
def create_user(data):
    try:
        # 데이터 검증 및 역직렬화
        user_data = employee_schema.load(data)
        
        # 이메일 중복 체크
        existing_user = Employee.query.filter_by(email=user_data['email']).first()
        if existing_user:
            return {"error": "Email already exists."}, 400

        # 고정 비밀번호 설정
        user_data['password'] = 'igloo1234'

        new_user = Employee(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Employee created", "user": {"id": new_user.id, "name": new_user.name}}, 201
    except ValidationError as err:
        return {"error": err.messages}, 400
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

    

       
        

   