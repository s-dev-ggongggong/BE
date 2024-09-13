from models.event_log import EventLog
from models.training import Training
from models.employee import Employee
from models.department import Department
from models.email import Email
from datetime import datetime
import json

def process_event(event_data, session):
    processed = {}
    for key, value in event_data.items():
        snake_key = key  # Use the original key as is
        if snake_key == 'id':
            continue
        processed[snake_key] = process_field(snake_key, value, session)
    return processed if validate_event(processed, session) else None

def process_field(key, value, session):
    if key in ['employee_id', 'email_id']:
        return ','.join(map(str, value if isinstance(value, list) else [value]))
    elif key in ['department_id', 'role_id']:
        return value[0] if isinstance(value, list) else value
    elif key == 'timestamp':
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif key == 'data':
        return value if value in ["", "agent"] else json.dumps(value)
    return value

def validate_event(event, session):
    department = session.get(Department, event['department_id'])
    if not department:
        print(f"Warning: Department ID {event['department_id']} not found")
        return False
    
    event['employee_id'] = validate_ids(Employee, event['employee_id'], session)
    event['email_id'] = validate_ids(Email, event['email_id'], session)
    
    return True

def validate_ids(model, ids, session):
    valid_ids = []
    for id in ids.split(','):
        if session.get(model, int(id)):
            valid_ids.append(id)
        else:
            print(f"Warning: {model.__name__} ID {id} not found")
    return ','.join(valid_ids)

def handle_events(events_data, session):
    for event_data in events_data:
        processed_event = process_event(event_data, session)
        if processed_event:
            update_or_create_event(processed_event, session)

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
