from sqlalchemy.orm import validates
from extensions import db
from models.base_model import BaseModel
from datetime import datetime
import json
from utils.http_status_handler import handle_response, server_error
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
import logging

from sqlalchemy.orm import validates
from marshmallow import fields, pre_load, post_dump, ValidationError

logger = logging.getLogger(__name__)

 

class EventLog(BaseModel):
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    department_id = db.Column(db.Text, nullable=False)  # JSON 문자열로 저장
    data = db.Column(db.Text, nullable=True, default="")

    training = db.relationship('Training', back_populates='event_logs')
 
    @property
    def department_id_list(self):
        return [int(x) for x in json.loads(self.department_id) if str(x).isdigit()]
    
    @department_id_list.setter
    def department_id_list(self, value):
        self.department_id = json.dumps([str(x) for x in value])

    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'trainingId': self.training_id,
            'departmentId': json.loads(self.department_id),
            'data': self.data
        }

    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value
    
    def __repr__(self):
        return f'<EventLog {self.action}>'