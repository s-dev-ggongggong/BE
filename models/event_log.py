from sqlalchemy.orm import validates
from extensions import db
from models.base_model import BaseModel
from datetime import datetime
import json
from utils.http_status_handler import handle_response, server_error
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
import logging

logger = logging.getLogger(__name__)



class EventLog(BaseModel):
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    department_id = db.Column(db.Integer,db.ForeignKey('departments.id'),nullable=False)
    data = db.Column(db.Text, nullable=True, default="")

    training = db.relationship('Training', backref='event_logs')

 
 

    def to_dict(self):
        def safe_json_loads(value):
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return []

        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'trainingId': self.training_id,
            'departmentId': safe_json_loads(self.department_id),
            'data': self.data
        }

    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value
    
    def __repr__(self):
        return f'<EventLog {self.action}>'