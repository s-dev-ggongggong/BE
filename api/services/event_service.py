#api/services/event_serivce.py
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.event_log import EventLog
from models.role import Role
from models.training import Training
from models.department import Department
from models.email import Email
from models.employee import Employee
from datetime import datetime
from flask import json



def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)

def to_camel_case(data):
    return {camelcase(k): v for k, v in data.items()}

def handle_event_log(training_id, data=None):
    try:
        training = Training.query.get(training_id)
        if not training:
            return {'error': 'Training not found'}, 404

        now = datetime.utcnow()
        timestamp = training.training_end if now > training.training_end else training.training_start
        action = 'remove' if now > training.training_end else 'targetSetting'
 
        event_data = {
            'training_id': training_id,
             'department_id': str(training.department_id),
            'employee_id': json.dumps([emp.id for emp in training.employees]),
            'email_id': json.dumps([email.id for email in training.emails]),
            'role_id': json.dumps([role.id for role in training.roles]),
            'timestamp': timestamp,
            'action': action,
            'data': data if data is not None else ""
        }

        existing_event = EventLog.query.filter_by(training_id=training_id).first()
        
        if existing_event:
            for key, value in event_data.items():
                setattr(existing_event, key, value)
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
def handle_multiple_events(training_ids, data=None):
    results = []
    for training_id in training_ids:
        result, status = handle_event_log(training_id, data)
        results.append({"training_id": training_id, "result": result, "status": status})
    return results


def delete_event_log(id):
    try:
        event_log = EventLog.query.get(id)
        if not event_log:
            return {'error': 'Event log not found'}, 404
        
        db.session.delete(event_log)
        db.session.commit()
        return {'message': 'Event log deleted', 'id': id}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_all_event_logs():
    try:
        event_logs = EventLog.query.all()
        return [to_camel_case(log.to_dict()) for log in event_logs], 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def get_event_log_by_id(id):
    try:
        event_log = EventLog.query.get(id)
        if not event_log:
            return {'error': 'Event log not found'}, 404
        return to_camel_case(event_log.to_dict()), 200
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500