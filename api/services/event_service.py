from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.event_log import EventLog
from models.training import Training
from models.department import Department
from models.email import Email
from models.employee import Employee
from datetime import datetime
from flask import json

def handle_event_log(training_id, data=None):
    try:
        training = Training.query.get(training_id)
        if not training:
            return {'error': 'Training not found'}, 404

        now = datetime.utcnow()
        timestamp = training.training_end if now > training.training_end else training.training_start
        action = 'remove' if now > training.training_end else 'targetSetting'

        # 관련된 데이터 가져오기
        department = Department.query.filter_by(id=training.department_id).first()
        employees = Employee.query.filter_by(department_id=training.department_id).all()
        emails = Email.query.filter_by(department_id=training.department_id).all()
        roles = Role.query.filter_by(department_id=training.department_id).all()

        event_data = {
            'training_id': training_id,
            'department_id': department.id if department else None,
            'employee_id': [emp.id for emp in employees],
            'email_id': [email.id for email in emails],
            'role_id': [role.id for role in roles],
            'timestamp': timestamp,
            'action': action,
            'data': data if data is not None else {}
        }

        existing_event = EventLog.query.filter_by(training_id=training_id).first()
        
        if existing_event:
            for key, value in event_data.items():
                setattr(existing_event, key, json.dumps(value) if isinstance(value, list) else value)
            db.session.commit()
            return {'message': 'Event log updated', 'id': existing_event.id}, 200
        else:
            new_event = EventLog(**event_data)
            db.session.add(new_event)
            db.session.commit()
            return {'message': 'Event log created', 'id': new_event.id}, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# Get all event logs
def get_all_event_logs():
    try:
        event_logs = EventLog.query.all()
        return [log.to_dict() for log in event_logs], 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

 

 
        
 # Get event log by ID
def get_event_log_by_id(event_log_id):
    try:
        event_log = EventLog.query.get(event_log_id)
        if not event_log:
            return {"error": "Event log not found"}, 404
        return event_log.to_dict(), 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500
    

def delete_event_log(event_id):
    try:
        event_log = EventLog.query.get(event_id)
        if not event_log:
            return {"error": "Event log 없습니다"}, 404
        db.session.delete(event_log)
        db.session.commit()
        return {"message": "Event log 삭제성공"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

 
def handle_multiple_events(training_ids, data=None):
    results = []
    for training_id in training_ids:
        result, status = handle_event_log(training_id, data)
        results.append({"data": result, "status": status})
    return results

def delete_multiple_events(event_ids):
    results = []
    for event_id in event_ids:
        result, status = delete_event_log(event_id)
        results.append({"data": result, "status": status})
    return results

 
def create_multiple_events(events_data):
    created_events = []
    for event_data in events_data:
        result, status = create_event(event_data)
        created_events.append({"data": result, "status": status})
    return created_events

def delete_multiple_events(event_ids):
    deleted_events = []
    for event_id in event_ids:
        result, status = delete_event_log(event_id)
        deleted_events.append({"data": result, "status": status})
    return deleted_events