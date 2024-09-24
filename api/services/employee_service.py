# File: api/services/employee_service.py

from marshmallow import ValidationError
from models.department import Department
from models.employee import Employee
from models.role import Role
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from utils.http_status_handler import handle_response ,server_error,unauthorized
from flask_jwt_extended import create_access_token
from utils.string_utils import convert_dict_keys_to_snake_case
from sqlalchemy import or_, func
from flask import current_app
from models.schemas import employee_schema, EmployeeSchema
# services/employee_service.py
def get_employees_by_filters(role_name=None, department_filters=None):
  query = Employee.query
  if role_name:
        query = query.filter(Employee.role_name == role_name)
  if department_filters:
    query = query.join(Employee.department).filter(*department_filters)
  employees = query.all()



def get_users(department=None, role_id=None, employee_id=None, search=None, role_name=None):
    try:
        query = db.session.query(
            Employee.id,
            Employee.name,
            Employee.email,
            Employee.role_name,
            Employee.role_eng_name,
            Employee.department_name,
            Employee.department_code1,
            Employee.department_code2
        )

        if employee_id:
            query = query.filter(Employee.id == employee_id)

        if department:
            normalized_dept = department.strip().upper()

            # Attempt to find the department by name, korean_name, code1, or code2
            dept = Department.query.filter(
                or_(
                    func.upper(Department.name) == normalized_dept,
                    func.upper(Department.korean_name) == normalized_dept,
                    Department.code1.ilike(f'%{department}%'),
                    Department.code2.ilike(f'%{department}%')
                )
            ).first()

            if dept:
                # Assuming department_id exists in Employee model
                query = query.filter(Employee.department_name  == dept.name)
            else:
                return {"message": f"부서를 찾을 수 없습니다: {department}"}, 404

        if role_id:
            role = Role.query.get(role_id)
            if role:
                query = query.filter(
                    or_(
                        Employee.role_name == role.korean_name,
                        Employee.role_eng_name == role.name
                    )
                )

        if role_name:
            role_name = role_name.replace('%20', ' ').strip()
            query = query.filter(
                or_(
                     func.lower(Employee.role_name) == func.lower(role_name),
                     func.lower(Employee.role_eng_name) == func.lower(role_name)
                )
            )

        if search:
            query = query.filter(Employee.name.ilike(f'%{search}%'))

        employees = query.all()
        query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
        current_app.logger.debug(f"Generated SQL query: {query_str}")

        if not employees:
            return {"message": f"직원을 찾을 수 없습니다. (Department: {department}, Role: {role_name})"}, 404

        result = [
            {
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "role_name": emp.role_name,
                "role_eng_name": emp.role_eng_name,
                "department_name": emp.department_name,
                "department_code1": emp.department_code1,
                "department_code2": emp.department_code2
            } for emp in employees
        ]

        return result, 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving users: {str(e)}", exc_info=True)
        return {"error": f"사용자 조회 중 오류 발생: {str(e)}"}, 500

def create_user(data):
    try:
        user_data = employee_schema.load(data)
        
        existing_user = Employee.query.filter_by(email=user_data['email']).first()
        if existing_user:
            return {"error": "Email already exists."}, 400

        input_role_name = user_data.get('role_name')
        role = Role.query.filter(or_(Role.name == input_role_name, Role.korean_name == input_role_name)).first()
        
        if not role:
            return {"error": "Invalid role name."}, 400

        user_data['role_name'] = role.korean_name
        user_data['role_eng_name'] = role.name

        user_data['password'] = 'igloo1234'  # Fixed password setting

        new_user = Employee(**user_data)
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "Employee created", "user": {"id": new_user.id, "name": new_user.name, "role": {"name": new_user.role_name, "eng_name": new_user.role_eng_name}}}, 201
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
    if admin_id == 'admin' and admin_pw == 'admin1234':
        access_token = create_access_token(identity=admin_id)
        admin_info = {
            "id": 1,
            "name": 'ADMIN',
            "email": 'admin@example.com',
            "department_name": '정보기술부',
            "role_name": 'IT 관리자',
            "is_admin": True
        }
        return {"status": 200, "data": {"access_token": access_token, "admin_info": admin_info}, "message": "로그인 성공"}, 200
    return {"status": 401, "message": "잘못된 관리자 정보"}, 401
    

       
        

   