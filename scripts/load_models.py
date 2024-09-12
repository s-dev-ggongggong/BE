import sys
import os

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from config import Config

# Initialize Flask and SQLAlchemy
from app import app
from extensions import db
from datetime import datetime

# Import models
from models.init import Department, Role, Employee, Email, Training 

def load_json(file_path):
    full_path = os.path.join(project_root, 'data', file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    with open(full_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Loaded {len(data)} items from {file_path}")
    return data



def process_emails(emails_data):
    processed_emails = []
    for email in emails_data:
        # Parse the 'date' field, assuming it matches the format '%Y-%m-%d %H:%M:%S'
        try:
            sent_date = email.get('date')  # Assuming 'date' field is used
            if sent_date:
                sent_date = datetime.strptime(sent_date, '%Y-%m-%d %H:%M:%S')
            else:
                sent_date = None
        except ValueError:
            print(f"Error parsing date {sent_date}: time data '{sent_date}' does not match format '%Y-%m-%d %H:%M:%S'")
            sent_date = None  # Handle error case

        # Process the email and store in the processed list
        processed_email = {
            'subject': email.get('subject'),
            'body': email.get('body'),
            'sender': email.get('from'),
            'recipient': email.get('to'),
            'sent_date': sent_date,
            'is_phishing': False  # Add any other logic you need for this field
        }
        processed_emails.append(processed_email)
    
    return processed_emails


def process_trainings(trainings_data):
    for training in trainings_data:
        print(f"Raw training data: {training}")  # 디버깅을 위해 원본 데이터 출력
        
        training['training_name'] = training.pop('trainingName', training.get('training_name'))
        training['training_desc'] = training.pop('trainingDesc', training.get('training_desc'))
        
        # 날짜 형식 변경
        training['training_start'] = datetime.strptime(training.pop('trainingStart', training.get('training_start')), '%Y-%m-%d %H:%M:%S')
        training['training_end'] = datetime.strptime(training.pop('trainingEnd', training.get('training_end')), '%Y-%m-%d %H:%M:%S')
        
        resource_user = training.pop('resourceUser', training.get('resource_user'))
        if resource_user is not None:
            if resource_user == 'RANDOM':
                training['resource_user'] = 1
            else:
                try:
                    resource_user_int = int(resource_user)
                    if resource_user_int < 1:
                        raise ValueError("resourceUser must be at least 1")
                    training['resource_user'] = resource_user_int
                except ValueError as e:
                    print(f"Invalid resourceUser value: {resource_user}. {str(e)}")
                    training['resource_user'] = 1  # 기본값 설정
        else:
            print("resourceUser not found, setting to default value 1")
            training['resource_user'] = 1  # 기본값 설정
        
        training['max_phishing_mail'] = training.pop('maxPhishingMail', training.get('max_phishing_mail', 0))
        training['dept_target'] = ','.join(training.pop('deptTarget', training.get('dept_target', [])))
        training['role_target'] = ','.join(training.pop('roleTarget', training.get('role_target', [])))
        
        # created_at 필드 처리 (있다면)
        if 'created_at' in training:
            training['created_at'] = datetime.strptime(training['created_at'], '%Y-%m-%d %H:%M:%S')
        
        print(f"Processed training data: {training}")  # 처리된 데이터 출력

    
    return trainings_data



def insert_or_update(session, model, data, unique_field):
    for item in data:
        existing = session.query(model).filter_by(**{unique_field: item[unique_field]}).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            new_item = model(**item)
            session.add(new_item)
    session.commit()
    print(f"Processed {len(data)} items for {model.__name__}")
    
def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

        insert_or_update(db.session, Department, load_json('departments.json'), 'name')
        insert_or_update(db.session, Role, load_json('roles.json'), 'name')
        
        employees_data = load_json('employees.json')
        for employee_data in employees_data:
            existing = Employee.query.filter_by(email=employee_data['email']).first()
            if existing:
                for key, value in employee_data.items():
                    setattr(existing, key, value)
                print(f"Updated employee: {existing.name}")
            else:
                new_employee = Employee(**employee_data)
                db.session.add(new_employee)
                print(f"Added new employee: {new_employee.name}")

            if employee_data['name'] == 'admin':
                existing = existing or new_employee
                existing.admin_id = 'admin'
                existing.admin_pw = 'admin1234'
                print("Admin credentials set")

        try:
            db.session.commit()
            print("All employees data saved successfully")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving employees data: {str(e)}")

        print("All initial data loaded successfully")

if __name__ == '__main__':
    init_db()