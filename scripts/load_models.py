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

# Import models
from models.init import Department, Role, Employee, Email, Training,AuthToken

def load_json(file_path):
    full_path = os.path.join(project_root, 'data', file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    with open(full_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Loaded {len(data)} items from {file_path}")
    return data

def insert_or_update(session, model, data, unique_field):
    added = updated = 0
    for item in data:
        existing = session.query(model).filter_by(**{unique_field: item[unique_field]}).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
            updated += 1
        else:
            new_item = model(**item)
            session.add(new_item)
            added += 1
    
    try:
        session.commit()
        print(f"Successfully processed {model.__name__}: Added {added}, Updated {updated}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error processing {model.__name__} data: {str(e)}")

def process_emails(emails_data):
    processed_emails = []
    for email in emails_data:
        processed_email = {
            'subject': email.get('subject'),
            'body': email.get('body'),
            'sender': email.get('from', email.get('sender')),
            'recipient': email.get('to', email.get('recipient')),
            'sent_date': None,
            'is_phishing': False,  # 기본값으로 설정
            'employee_id': 1  # 임시로 1로 설정, 실제 구현에서는 적절한 employee_id를 찾아야 합니다
        }
        
        sent_date = email.get('date') or email.get('sentDate')
        if sent_date:
            try:
                if '+' in sent_date:
                    # "Mon, 02 Sep 2024 08:12:53 +0000" 형식 처리
                    processed_email['sent_date'] = datetime.strptime(sent_date, '%a, %d %b %Y %H:%M:%S %z')
                else:
                    # "2023-09-02T00:00:00Z" 형식 처리
                    processed_email['sent_date'] = datetime.strptime(sent_date, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                print(f"Error parsing date {sent_date}: {e}")
                processed_email['sent_date'] = datetime.utcnow()  # 파싱 실패 시 현재 시간으로 설정
        else:
            processed_email['sent_date'] = datetime.utcnow()  # 날짜 정보가 없을 경우 현재 시간으로 설정
        
        processed_emails.append(processed_email)
    
    return processed_emails
def process_trainings(trainings_data):
    for training in trainings_data:
        print(f"Raw training data: {training}")  # 디버깅을 위해 원본 데이터 출력
        
        training['training_name'] = training.pop('trainingName', training.get('training_name'))
        training['training_desc'] = training.pop('trainingDesc', training.get('training_desc'))
        training['training_start'] = datetime.strptime(training.pop('trainingStart', training.get('training_start')), '%Y-%m-%d').date()
        training['training_end'] = datetime.strptime(training.pop('trainingEnd', training.get('training_end')), '%Y-%m-%d').date()
        
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
        
        print(f"Processed training data: {training}")  # 처리된 데이터 출력
    
    return trainings_data

def process_auth_tokens(tokens_data):
    processed_tokens = []
    for token in tokens_data:
        processed_token = {
            'token': token['token'],
            'employee_id': token['employee_id'],
            'created_at': datetime.strptime(token['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            'expires_at': datetime.strptime(token['expires_at'], '%Y-%m-%dT%H:%M:%SZ')
        }
        processed_tokens.append(processed_token)
    return processed_tokens


def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

        # Load data in order to respect foreign key constraints
        insert_or_update(db.session, Department, load_json('departments.json'), 'name')
        insert_or_update(db.session, Role, load_json('roles.json'), 'name')
        
        employees_data = load_json('employees.json')
        for employee in employees_data:
            if 'password' not in employee:
                employee['password'] = 'default_password'
        insert_or_update(db.session, Employee, employees_data, 'email')
        
        try:
            emails_data = process_emails(load_json('emails.json'))
            for email_data in emails_data:
                existing_email = Email.query.filter_by(subject=email_data['subject'], sender=email_data['sender']).first()
                if existing_email:
                    for key, value in email_data.items():
                        setattr(existing_email, key, value)
                else:
                    new_email = Email(**email_data)
                    db.session.add(new_email)
            db.session.commit()
            print(f"Successfully processed {len(emails_data)} emails")
        except Exception as e:
            db.session.rollback()
            print(f"Error processing emails: {str(e)}")
        
        insert_or_update(db.session, Training, process_trainings(load_json('trainings.json')), 'training_name')

        # Load AuthToken data
        try:
            auth_tokens_data = process_auth_tokens(load_json('tokens.json'))
            for token_data in auth_tokens_data:
                existing_token = AuthToken.query.filter_by(token=token_data['token']).first()
                if existing_token:
                    for key, value in token_data.items():
                        setattr(existing_token, key, value)
                else:
                    new_token = AuthToken(**token_data)
                    db.session.add(new_token)
            db.session.commit()
            print(f"Successfully processed {len(auth_tokens_data)} auth tokens")
        except Exception as e:
            db.session.rollback()
            print(f"Error processing auth tokens: {str(e)}")

        print("All initial data loaded successfully")
     
if __name__ == '__main__':
    init_db()