from models.event_log import EventLog
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from utils.http_status_handler import handle_response, server_error, not_found, bad_request
from api.services.training_service import check_and_set_action_for_email
  # 수정 후



# Get all event logs
def get_all_event_logs():
    try:
        event_logs = EventLog.query.all()
        result = [
            {
                "id": event_log.id,
                "details": event_log.details,
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
        if not data or not data.get('training_id') or not data.get('employee_id') or not data.get('department_id'):
            return bad_request("Missing required fields: training_id, employee_id, department_id")

        new_event_log = EventLog(
            details=data.get('details'),
            training_id=data['training_id'],
            employee_id=data['employee_id'],
            department_id=data['department_id'],
            action=data['action']
        )
        db.session.add(new_event_log)
        db.session.commit()

        return handle_response(201, data={
            "id": new_event_log.id,
            "action": new_event_log.action
        }, message="Event log created successfully")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(str(e))

# Get event log by ID
def get_event_log_by_id(event_log_id):
    try:
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return not_found(f"Event log with ID {event_log_id} not found")

        return handle_response(200, data={
            "id": event_log.id,
            "details": event_log.details,
            "training_id": event_log.training_id,
            "employee_id": event_log.employee_id,
            "department_id": event_log.department_id,
            "action": event_log.action,
            "timestamp": event_log.timestamp
        }, message=f"Event log ID {event_log_id} fetched successfully")
    except SQLAlchemyError as e:
        return server_error(str(e))

# Update an event log
def update_event_log(event_log_id, data):
    try:
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return not_found(f"Event log with ID {event_log_id} not found")

        event_log.details = data.get('details', event_log.details)
        event_log.action = data.get('action', event_log.action)

        db.session.commit()
        return handle_response(200, data={
            "id": event_log.id,
            "action": event_log.action
        }, message=f"Event log ID {event_log_id} updated successfully")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(str(e))

# Delete an event log
def delete_event_log(event_log_id):
    try:
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return not_found(f"Event log with ID {event_log_id} not found")

        db.session.delete(event_log)
        db.session.commit()
        return handle_response(200, message=f"Event log ID {event_log_id} deleted successfully")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(str(e))
