from sqlalchemy.orm import validates
from extensions import db
from models.base_model import BaseModel
from datetime import datetime
import json

class EventLog(BaseModel):
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    training_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    employee_id = db.Column(db.String(255))
    email_id = db.Column(db.String(255))
    role_id = db.Column(db.Integer)
    data = db.Column(db.Text,nullable=True,default="")

    @validates('action')
    def validate_action(self, key, action):
        allowed_actions = [ 'remove', 'targetSetting']
        assert action in allowed_actions, f"Invalid action: {action}"
        return action
    def set_data(self, data_dict):
        self.data = data_dict

    @classmethod
    def required_fields(cls):
        return ['action', 'timestamp', 'training_id', 'data']
    

    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None,
            'training_id': self.training_id,
            'department_id': self.department_id if isinstance(self.department_id) else [],  
            'employee_id': self.employee_id if isinstance(self.employee_id) else [],  # Ensure list,
            'email_id': self.email_id if isinstance(self.email_id) else [],  # Ensure list,
            'role_id': self.role_id if isinstance(self.role_id) else [],  # Ensure list,
            'data': self.data  if self.data is not None else ""
            
        }
    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value
    def __repr__(self):
        return f'<EventLog {self.event_type}>'