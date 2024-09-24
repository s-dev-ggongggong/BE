import json
import re
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from models.training import Training
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
        existing = Role.query.filter_by(name=item['name']).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            role = Role(**item)
            db.session.add(role)
    db.session.commit()


def load_trainings(training_data):
    for item in training_data:
        try:
            # Convert keys to snake_case
            item = convert_keys_to_snake_case(item)
            
            # Convert date strings to datetime objects
            item['training_start'] = convert_date_string_to_datetime(item['training_start'])
            item['training_end'] = convert_date_string_to_datetime(item['training_end'])

            # Create Training object and add to session
            training = Training(**item)
            db.session.add(training)
        except SQLAlchemyError as e:
            print(f"An error occurred while adding training: {e}")
            db.session.rollback()   



def load_employees(data):
    departments = {d.korean_name: d.id for d in Department.query.all()}
    roles = {r.korean_name: r.id for r in Role.query.all()}

    for item in data:
        department_id = departments.get(item['department_name'])
        role_id = roles.get(item['role_name'])

        if department_id is None or role_id is None:
            print(f"Warning: Department or Role not found for employee {item['name']}")
            continue

        try:
            employee = Employee(
                name=item['name'],
                email=item['email'],
                password=item['password'],  # Hash password for secure storage
                department_id=department_id,
                role_id=role_id,
                is_admin=item['name'] == 'ADMIN'
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
            'sender': item['from'],  # Changed from 'from' to 'sender'
            'recipient': item['to'],  # Changed from 'to' to 'recipient'
            'sent_date': convert_date_string_to_datetime(item['date']),  # Changed from 'date' to 'sent_date'
            'making_phishing': 0  # 기본값 설정

        }

        email = Email(**email_data)
        db.session.add(email)
    db.session.commit()

def load_event_logs(event_logs):
    for item in event_logs:
        event_log_data = {
            'action': item['action'],
            'timestamp': convert_date_string_to_datetime(item['timestamp']),
            'training_id': item['trainingId'],
            'employee_id': ','.join(map(str, item['employeeId'])),
            'department_id': ','.join(map(str, item['departmentId'])),
            'email_id': ','.join(map(str, item['emailId'])),
            'role_id': ','.join(map(str, item['roleId'])),
            'data': item['data']
        }
        
        event_log = EventLog(**event_log_data)
        db.session.add(event_log)
    
    db.session.commit()

# Call the function to load event logs

    
def main():
    app = create_app()
    with app.app_context():
        db.session.query(Employee).delete()
        db.session.query(Training).delete()  # Clear existing data if necessary
        db.session.commit()

        departments = load_json('data/departments.json')
        load_departments(departments)

        roles = load_json('data/roles.json')
        load_roles(roles)

       

        employees = load_json('data/employees.json')
        load_employees(employees)
        print("Employee data successfully loaded.")

        trainings = load_json('data/trainings.json')
        load_trainings(trainings)
       
        emails = load_json('data/emails.json')
        load_emails(emails)


        events = load_json('data/event_logs.json')
        load_event_logs(events)

        
        print("Data successfully loaded.")

 
        print("All trainings have been successfully added.")
 
 
if __name__ == '__main__':
    main()
