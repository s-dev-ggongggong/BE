import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError ,IntegrityError
from extensions import db
from models.event_log import EventLog
from models.training import Training
from models.employee import Employee
from models.department import Department
from models.email import Email
from app import create_app
import re


def parse_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def ensure_list(field):
    """Ensure the field is a properly formatted list."""
    if isinstance(field, str):
        # Clean up and convert string-formatted lists like "[1, 2]" to actual lists
        field = field.strip("[]")  # Remove the square brackets
        field = [int(x.strip()) for x in field.split(",") if x.strip()]  # Split and convert to list of integers
    elif isinstance(field, int):
        # Convert single integer to list
        return [field]
    return field if isinstance(field, list) else [field]


def process_event(event_data, session):
    """Process each event data to ensure it is correctly formatted for insertion."""
    if isinstance(event_data, EventLog):
        event_data = event_data.to_dict()
    
    # Convert camelCase keys to snake_case
    event_data = {camel_to_snake(k): v for k, v in event_data.items()}
    event_data.pop('id', None)

    # Ensure 'training_id' exists and is properly processed
    if 'training_id' not in event_data or not event_data['training_id']:
        print("Warning: Missing 'training_id' in event data.")
        return None

    for field in ['department_id']:
        if field in event_data:
            event_data[field] = json.dumps(ensure_list(event_data.get(field, [])))

    if 'timestamp' in event_data and isinstance(event_data['timestamp'], str):
        event_data['timestamp'] = datetime.strptime(event_data['timestamp'], '%Y-%m-%d %H:%M:%S')    
    
    event_data['data'] = event_data.get('data', "").strip("\"")
    # Convert lists to comma-separated strings for IDs
 
    return event_data


def load_event_logs(file_path):
    app = create_app()
    with app.app_context():
        with open(file_path, 'r') as file:
            event_logs = json.load(file)
            

        for log in event_logs:
            try:
                # Safely handle trainingId as either string or integer
                training_id = log.get('trainingId')
                if isinstance(training_id, str):
                    training_id = int(training_id) if training_id.isdigit() else None
                elif isinstance(training_id, int):
                    training_id = training_id
                else:
                    training_id = None  # Handle any other unexpected format

                # Map log fields to EventLog model attributes
                event = EventLog(
                    id=log.get('id'),
                    action=log.get('action'),
                    timestamp=log.get('timestamp'),
                    training_id=training_id,
                    department_id=log.get('departmentId'),  # Assuming department_id is a list of integers
                    data=log.get('data')
                )

                # Add event log to session
                db.session.add(event)

            except IntegrityError as e:
                db.session.rollback()
                print(f"Integrity error while processing log ID {log.get('id')}: {str(e)}")

            except Exception as e:
                db.session.rollback()
                print(f"Error processing log ID {log.get('id')}: {str(e)}")

        # Commit the session after processing all logs
        try:
            db.session.commit()
            print("All event logs loaded successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing session: {str(e)}")

# Run the function with the updated event logs JSON path
 

def process_field(key, value, session):
    
    if key in [ 'department_id' ]:
        if isinstance(key, str):
            return json.dumps(value if isinstance(value, list) else [value])
    elif key == 'department_id':
        return value[0] if isinstance(value, list) else value
    elif key == 'timestamp':
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError as ve:
            print(f"Warning: Invalid timestamp format '{value}': {ve}")
            return None
    elif key == 'data':
        return json.dumps(value) if value not in ["", "agent"] else value
    return value

# Rest of the code remains the same...

def validate_event(event, session):
    department_id = event.get('department_id')
    if not department_id:
        print("Warning: 'department_id' is missing in the event data.")
        return False

    department = session.get(Department, department_id)
    if not department:
        print(f"Warning: Department ID {department_id} not found")
        return False
    
 
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
        training_id=event_data['training_id']
    ).first()

    if existing_event:
        for key, value in event_data.items():
            setattr(existing_event, key, value)
    else:
        new_event = EventLog(**event_data)
        session.add(new_event)


def handle_events(events_data, session):
    """Handle multiple events data."""
    for event_data in events_data:
        processed_event = process_event(event_data, session)
        if processed_event:  # Ensure that None values are not processed
            update_or_create_event(processed_event, session)
        else:
            print(f"Skipping event due to missing training_id: {event_data}")

 

if __name__ == '__main__':
    load_event_logs('data/event_logs.json')
