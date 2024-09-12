from models.event_log import EventLog
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import event_log_schema
from utils.http_status_handler import handle_response, server_error, not_found, bad_request
from datetime import datetime
  # 수정 후

def check_duplicate_event_log(data):
    """
    Check if an event log with the same data (except for 'id' and 'timestamp') already exists.
    """
    return EventLog.query.filter_by(
        action=data.get('action'),
        training_id=data.get('trainingId'),
        message=data.get('message')
    ).first()

# Get all event logs
def get_all_event_logs():
    try:
        event_logs = EventLog.query.all()
        result = [
            {
                "id": event_log.id,
                "data": event_log.data,
                "training_id": event_log.training_id,
                "employee_id": event_log.employee_id,
                "department_id": event_log.department_id,
                "action": event_log.action,
                "timestamp": event_log.timestamp
            }
            for event_log in event_logs
        ]
        return handle_response(200, data=result, message="Event logs fetched successfully")
    except SQLAlchemyError as e:
        return server_error(str(e))

# Create a new event log
def create_new_event_log(data):
    try:
        duplicate_log = check_duplicate_event_log(data)
        if duplicate_log:
            return {"message": "Duplicate event log already exists"}, 400

        # Parse timestamp with fallback if missing or incorrectly formatted
        timestamp = datetime.strptime(data.get('timestamp', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')

        new_event_log = EventLog(
            action=data['action'],
            timestamp=timestamp,
            training_id=data.get('trainingId'),
            message=data.get('message', '')
        )
        db.session.add(new_event_log)
        db.session.commit()

        return event_log_schema.dump(new_event_log), 201  # Ensure event_log_schema is correctly defined
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


# Get event log by ID
def get_event_log_by_id(event_log_id):
    try:
   
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return not_found(f"Event log with ID {event_log_id} not found")
        
        # Serialize the event log
        return {
            "id": event_log.id,
            "data": event_log.data,
            "training_id": event_log.training_id,
            "employee_id": event_log.employee_id,
            "department_id": event_log.department_id,
            "action": event_log.action,
            "timestamp": event_log.timestamp.isoformat()  # Ensure timestamp is serialized
        }, 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

# Update an event log
 
def update_event_log(event_log_id, data):
    try:
    
        # Fetch the existing event log
        existing_log = EventLog.query.get(event_log_id)
        if not existing_log:
            return not_found(f"Event log with ID {event_log_id} not found"), 404
        duplicate_log = EventLog.query.filter(
            EventLog.training_id == data.get('trainingId'),
            EventLog.message == data.get('message'),
            EventLog.id != event_log_id  # Exclude current record from duplicate check
        ).first()

        timestamp = datetime.strptime(data.get('timestamp', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')

        new_event_log = EventLog(
            action=existing_log.action,
            timestamp=timestamp,
            training_id=data.get('trainingId', existing_log.training_id),
            message=data.get('message', existing_log.message)
        )
        db.session.add(new_event_log)
        db.session.commit()

        return event_log_schema.dump(new_event_log), 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400

# Delete an event log
def delete_event_log(event_log_id):
    try:
        # Fetch the existing event log
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return {"message": f"Event log with ID {event_log_id} not found"}, 404

        # Delete the event log
        db.session.delete(event_log)
        db.session.commit()

        return {"message": f"Event log with ID {event_log_id} deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


 