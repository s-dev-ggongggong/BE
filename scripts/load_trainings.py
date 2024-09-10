import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# 경로 설정
app = Flask(__name__)

# SQLite 데이터베이스 파일 설정
db_path = os.path.join(os.path.dirname(__file__), 'db', 'e_sol.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 초기화
db = SQLAlchemy(app)

# 모델 정의 (간략하게 추가된 부분 포함)
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code1 = db.Column(db.String(10), nullable=False)
    code2 = db.Column(db.String(10), nullable=False)
    korean_name = db.Column(db.String(50), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    korean_name = db.Column(db.String(50), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_date = db.Column(db.DateTime, nullable=False)

class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

class Training(db.Model):
    __tablename__ = 'trainings'
    id = db.Column(db.Integer, primary_key=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.Date, nullable=False)
    training_end = db.Column(db.Date, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.String(255), nullable=False)
    role_target = db.Column(db.String(255), nullable=False)

# JSON 파일 로드 함수 정의
def load_json(file_path):
    # 파일 경로를 절대 경로로 변환
    file_path = os.path.join(os.path.dirname(__file__), '..', file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 각 테이블에 데이터 로드 함수 정의
def load_departments(departments_data):
    for dept in departments_data:
        existing_dept = Department.query.filter_by(code1=dept['code1']).first()
        if not existing_dept:
            new_dept = Department(
                name=dept['name'],
                code1=dept['code1'],
                code2=dept['code2'],
                korean_name=dept['korean_name']
            )
            db.session.add(new_dept)
    db.session.commit()

def load_roles(roles_data):
    for role in roles_data:
        existing_role = Role.query.filter_by(name=role['name']).first()
        if not existing_role:
            new_role = Role(
                name=role['name'],
                korean_name=role['korean_name']
            )
            db.session.add(new_role)
    db.session.commit()
 
# Load employees function with respect to role and department relationships
def load_employees(employees_data):
    # Check if the default role 'Employee' exists; if not, create it.
    default_role = Role.query.filter_by(name='Employee').first()
    if not default_role:
        default_role = Role(name='Employee', korean_name='사원')  # Assuming Korean name as '사원'
        db.session.add(default_role)
        db.session.commit()  # Commit to get the role ID

    # Check if the default department 'General' exists; if not, create it.
    default_department = Department.query.filter_by(name='General').first()
    if not default_department:
        default_department = Department(name='General', code1='GEN', code2='001', korean_name='일반')
        db.session.add(default_department)
        db.session.commit()  # Commit to get the department ID

    # Iterate over employee data and add them to the database
    for emp in employees_data:
        existing_emp = Employee.query.filter_by(email=emp['email']).first()
        if not existing_emp:
            new_emp = Employee(
                name=emp['name'],
                email=emp['email'],
                password='igloo1234',  # Fixed password as per your request
                role_id=default_role.id,
                department_id=default_department.id
            )
            db.session.add(new_emp)
    
    # Commit all new employee records to the database
    db.session.commit()


def load_emails(emails_data):
    for email in emails_data:
        # Handling different key names for sender, recipient, and date
        sender = email.get('sender', email.get('from'))  # Tries to get 'sender', falls back to 'from'
        recipient = email.get('recipient', email.get('to'))  # Tries to get 'recipient', falls back to 'to'
        sent_date_str = email.get('sentDate', email.get('date'))  # Tries to get 'sentDate', falls back to 'date'

        # Parse date in case it's provided in different formats
        try:
            sent_date = datetime.strptime(sent_date_str, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            sent_date = datetime.strptime(sent_date_str, '%a, %d %b %Y %H:%M:%S %z')  # Handling the "Mon, 02 Sep 2024" format

        # Check if the email already exists
        existing_email = Email.query.filter_by(
            sender=sender,
            recipient=recipient,
            subject=email['subject'],
            sent_date=sent_date
        ).first()

        if not existing_email:
            # Create new email instance
            new_email = Email(
                sender=sender,
                recipient=recipient,
                subject=email['subject'],
                body=email['body'],
                sent_date=sent_date
            )
            db.session.add(new_email)
    
    db.session.commit()
    print("Emails loaded successfully.")

def load_tokens(tokens_data):
    for token in tokens_data:
        existing_token = AuthToken.query.filter_by(token=token['token']).first()
        if not existing_token:
            new_token = AuthToken(
                token=token['token'],
                employee_id=token['employee_id'],
                created_at=datetime.fromisoformat(token['created_at']),
                expires_at=datetime.fromisoformat(token['expires_at'])
            )
            db.session.add(new_token)
    db.session.commit()

def load_trainings(trainings_data):
    for training in trainings_data:
        # Check if the training already exists based on the name
        existing_training = Training.query.filter_by(training_name=training['trainingName']).first()

        if not existing_training:
            # Create a new training instance
            new_training = Training(
                training_name=training['trainingName'],
                training_desc=training['trainingDesc'],
                training_start=datetime.strptime(training['trainingStart'], '%Y-%m-%d'),
                training_end=datetime.strptime(training['trainingEnd'], '%Y-%m-%d'),
                resource_user=1 if training['resourceUser'] == "RANDOM" else training['resourceUser'],  # Assuming 'RANDOM' is treated as 1
                max_phishing_mail=training['maxPhishingMail'],
                dept_target=json.dumps(training['deptTarget']),  # Storing the department target as a JSON string
                role_target=json.dumps(training['roleTarget'])  # Storing the role target as a JSON string
            )

            db.session.add(new_training)
    
    # Commit all new training records to the database
    db.session.commit()
    print("Trainings loaded successfully.")

# 메인 함수
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Load your data here
        departments_data = load_json('static/departments.json')
        roles_data = load_json('static/roles.json')
        employees_data = load_json('static/employees.json')
        emails_data = load_json('static/emails.json')
        tokens_data = load_json('static/tokens.json')
        trainings_data = load_json('static/trainings.json')

        load_departments(departments_data)
        load_roles(roles_data)
        load_employees(employees_data)
        load_emails(emails_data)
        load_tokens(tokens_data)
        load_trainings(trainings_data)

        print("Data loading complete!")
