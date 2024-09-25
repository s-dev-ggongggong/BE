import json
import re
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from models.training import Training, TrainingStatus
from models.department import Department
from models.employee import Employee
from models.email import Email
from models.role import Role
from models.event_log import EventLog
from app import create_app
import json
from datetime import datetime

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def convert_date_string_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def validate_targets(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        print(f"Invalid JSON data: {value}")
        return []
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

# Process JSON data to ensure all keys are converted
def process_data(json_data):
    return {camel_to_snake(k): v for k, v in json_data.items()}

def load_departments(data):
    for item in data:
        item = process_data(item)
        existing = Department.query.filter_by(name=item['name']).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            department = Department(**item)
            db.session.add(department)
    db.session.commit()

def load_roles(data):
    for item in data:
        item = process_data(item)
        role = Role.query.filter(or_(Role.name == item['name'], Role.korean_name == item['korean_name'])).first()
        if role:
            for key, value in item.items():
                setattr(role, key, value)
        else:
            role = Role(**item)
            db.session.add(role)
    db.session.commit()


def load_trainings(training_data):
    departments = {d.id: d.id for d in Department.query.all()}
    for item in training_data:
        item.pop('id', None) 
        item = convert_keys_to_snake_case(item)
        item['training_start'] = convert_date_string_to_datetime(item['training_start'])
        item['training_end'] = convert_date_string_to_datetime(item['training_end'])
        # JSON 변환 제거, 리스트 그대로 유지
        
        if item['dept_target']:
            dept_id = item['dept_target'][0]  # 첫 번째 부서 ID를 사용
            if dept_id in departments:
                item['department_id'] = dept_id
            else:
                print(f"Warning: Invalid department_id {dept_id} for training {item.get('training_name', 'Unknown')}")
                continue
        
        training = Training(**item)
        db.session.add(training)
    
    db.session.commit()
 

def load_employees(data):
    departments = {d.id: d for d in Department.query.all()}
    roles = {r.korean_name.strip(): r for r in Role.query.all()}

    # ADMIN 계정 먼저 처리
    admin_data = next(item for item in data if item['name'] == 'ADMIN')
    admin_role = roles.get(admin_data['role_name'].strip())
    admin_dept = departments.get(admin_data['department_id'])

    if not admin_role or not admin_dept:
        print("Error: ADMIN role or department not found")
        return

    admin = Employee.query.filter_by(name='ADMIN').first()
    if not admin:
        admin = Employee(
            id=1,
            name='ADMIN',
            email=admin_data['email'],
            password=admin_data['password'],
            department_id=admin_dept.id,
            role_id=admin_role.id,
            is_admin=True
        )
        db.session.add(admin)
    else:
        admin.email = admin_data['email']
        admin.password = admin_data['password']
        admin.department_id = admin_dept.id
        admin.role_id = admin_role.id
        admin.is_admin = True

    # 나머지 직원 처리
    for item in data:
        if item['name'] == 'ADMIN':
            continue

        role = roles.get(item['role_name'].strip())
        department = departments.get(item['department_id'])

        if not role or not department:
            print(f"Warning: Role or Department not found for employee {item['name']}")
            continue

        try:
            employee = Employee(
                name=item['name'],
                email=item['email'],
                password=item['password'],
                department_id=department.id,
                role_id=role.id,
                is_admin=False
            )
            db.session.add(employee)
        except SQLAlchemyError as e:
            print(f"Error adding employee {item['name']}: {e}")
            db.session.rollback()

    db.session.commit()
 

def load_emails(emails):
    for item in emails:
        # Convert the email data to the correct schema for the Email model
        email_data = {
        'subject': item['subject'],
        'body': item['body'],
        'sender': item['from'],
        'recipient': item['to'],
        'sent_date': convert_date_string_to_datetime(item['date']),
        'making_phishing': 0
        }

        email = Email(**email_data)
        db.session.add(email)
    db.session.commit()

# def load_event_logs(event_logs):
#     for item in event_logs:
#         event_log_data = {
#             'action': item['action'],
#             'timestamp': convert_date_string_to_datetime(item['timestamp']),
#             'training_id': item['trainingId'],
#             'employee_id': ','.join(map(str, item['employeeId'])),
#             'department_id': ','.join(map(str, item['departmentId'])),
#             'email_id': ','.join(map(str, item['emailId'])),
#             'role_id': ','.join(map(str, item['roleId'])),
#             'data': item['data']
#         }
        
#         event_log = EventLog(**event_log_data)
#         db.session.add(event_log)
    
#     db.session.commit()

# Call the function to load event logs

    
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
