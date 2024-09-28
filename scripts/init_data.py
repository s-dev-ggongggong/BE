import json
import re
from marshmallow import ValidationError
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from models.schemas import department_schema, employee_schema, role_schema ,email_schema
from models.training import Training, TrainingStatus
from models.department import Department
from models.employee import Employee
from models.email import Email
from models.role import Role
from models.event_log import EventLog
from models.schemas import training_schema
from app import create_app
import json
from datetime import datetime
 

import logging

logger = logging.getLogger(__name__)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def convert_date_string_to_datetime(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # ISO 형식 지원
        try:
            return datetime.fromisoformat(date_string)
        except ValueError as ve:
            raise ValueError(f"Unsupported date format: {date_string}") from ve


def initialize_db():
    db.drop_all()
    db.create_all()    

def camel_to_snake(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
# Convert camelCase keys to snake_case


def convert_keys_to_snake_case(data):
    """Convert keys in the dictionary to snake_case."""
    return {camel_to_snake(k): v for k, v in data.items()}
 
def load_departments(data):
    for item in data:
        try:
            department = department_schema.load(item, session=db.session)
            existing = Department.query.filter_by(name=department.name).first()
            if existing:
                for key, value in department_schema.dump(department).items():
                    setattr(existing, key, value)
            else:
                db.session.add(department)
        except ValidationError as err:
            print(f"Validation error for department {item.get('name', 'Unknown')}: {err}")
    try:
        db.session.commit()
        print("Departments loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error committing departments to the database: {e}")


def load_roles(data):
    for item in data:
        try:
            role = role_schema.load(item, session=db.session)
            existing = Role.query.filter(or_(Role.name == role.name, Role.korean_name == role.korean_name)).first()
            if existing:
                for key, value in role_schema.dump(role).items():
                    setattr(existing, key, value)
            else:
                db.session.add(role)
        except ValidationError as err:
            print(f"Validation error for role {item.get('name', 'Unknown')}: {err}")
    try:
        db.session.commit()
        print("Roles loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error committing roles to the database: {e}")

def load_trainings(training_data):
    for item in training_data:
        item.pop('id', None)
        print(f"처리 전 항목: {item}")
        if 'deptTarget' in item:
            item['dept_target'] = item.pop('deptTarget')
        print(f"처리 후 항목: {item}")
        
        try:
            print(f"스키마 로딩 직전 item: {item}")
            training = training_schema.load(item, session=db.session)
            db.session.add(training)
        except ValidationError as err:
            print(f"검증 오류 '{item.get('trainingName', '알수없음')}': {err.messages}")
        except SQLAlchemyError as e:
            print(f"DB 오류 '{item.get('trainingName', '알수없음')}': {e}")
            db.session.rollback()

    try:
        db.session.commit()
        print("트레이닝 데이터 로드 완료")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"DB 커밋 오류: {e}")

def load_employees(data):
    for item in data:
        try:
            employee = employee_schema.load(item, session=db.session)
            db.session.add(employee)
        except ValidationError as err:
            print(f"Validation error for employee {item.get('name', 'Unknown')}: {err.messages}")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"Error adding employee '{item.get('name', 'Unknown')}': {e}")
            db.session.rollback()
    try:
        db.session.commit()
        print("Employees loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error committing employees to the database: {e}")
        

def load_emails(emails):
    for item in emails:
        try:
            email = email_schema.load(item, session=db.session)
            db.session.add(email)
        except ValidationError as err:
            print(f"Validation error for email '{item.get('subject', 'Unknown')}': {err.messages}")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"Error adding email '{item.get('subject', 'Unknown')}': {e}")
            db.session.rollback()

    try:
        db.session.commit()
        print("Emails loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error committing emails to the database: {e}")

 
    
def main():
    app = create_app()
    with app.app_context():
        initialize_db()  # Clear existing data if necessary
         
        departments = load_json('data/departments.json')
        load_departments(departments)
        roles = load_json('data/roles.json')
        load_roles(roles)
        employees = load_json('data/employees.json')
        load_employees(employees)
        trainings = load_json('data/trainings.json')
        load_trainings(trainings)
        emails = load_json('data/emails.json')
        load_emails(emails)
        print("All data loaded successfully.")
 
if __name__ == '__main__':
    main()
