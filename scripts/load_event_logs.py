import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from models.event_log import EventLog
from models.training import Training
from models.employee import Employee
from models.department import Department
from models.email import Email
from app import create_app
import re

 
def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_event(event_data, session):
    processed = {}
    for key, value in event_data.items():
        snake_key = camel_to_snake(key)
        if snake_key == 'id':
            continue
        processed[snake_key] = process_field(snake_key, value, session)
    
    if 'department_id' not in processed:
        print(f"Warning: 'department_id' missing in event_data: {event_data}")
        return None

    return processed if validate_event(processed, session) else None

def process_field(key, value, session):
    if key in ['employee_id', 'email_id']:
        return ','.join(map(str, value if isinstance(value, list) else [value]))
    elif key in ['department_id', 'role_id']:
        return value[0] if isinstance(value, list) else value
    elif key == 'timestamp':
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError as ve:
            print(f"Warning: Invalid timestamp format '{value}': {ve}")
            return None
    elif key == 'data':
        return value if value in ["", "agent"] else json.dumps(value)
    return value

def validate_event(event, session):
    department_id = event.get('department_id')
    if not department_id:
        print("Warning: 'department_id' is missing in the event data.")
        return False

    department = session.get(Department, department_id)
    if not department:
        print(f"Warning: Department ID {department_id} not found")
        return False
    
    event['employee_id'] = validate_ids(Employee, event['employee_id'], session)
    event['email_id'] = validate_ids(Email, event['email_id'], session)
    
    return True

def validate_ids(model, ids, session):
    valid_ids = []
    for id in ids.split(','):
        try:
            id_int = int(id)
            if session.get(model, id_int):
                valid_ids.append(id)
            else:
                print(f"Warning: {model.__name__} ID {id} not found")
        except ValueError:
            print(f"Warning: Invalid ID format '{id}'")
    return ','.join(valid_ids)

def update_or_create_event(event_data, session):
    existing_event = EventLog.query.filter_by(
        action=event_data['action'],
        timestamp=event_data['timestamp'],
        training_id=event_data['training_id'],
        department_id=event_data['department_id'],
        employee_id=event_data['employee_id'],
        email_id=event_data['email_id'],
        role_id=event_data['role_id']
    ).first()

    if existing_event:
        if existing_event.data != event_data['data']:
            existing_event.data = event_data['data']
    else:
        new_event = EventLog(**event_data)
        session.add(new_event)

def handle_events(events_data, session):
    for event_data in events_data:
        processed_event = process_event(event_data, session)
        if processed_event:
            update_or_create_event(processed_event, session)

def load_event_logs(file_path):
    app = create_app()
    with app.app_context():
        try:
            db.session.query(EventLog).delete()  # Clear existing events
            db.session.commit()
            
            events_data = load_json(file_path)
            handle_events(events_data, db.session)
            
            db.session.commit()
            print(f"Processed and loaded {len(events_data)} events")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

if __name__ == '__main__':
    load_event_logs('data/event_logs.json')
