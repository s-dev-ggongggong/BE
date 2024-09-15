from extensions import db
from datetime import datetime
import json
from models.base_model import BaseModel
from enum import Enum
from sqlalchemy.orm import validates

class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"
class Training(BaseModel):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.DateTime, nullable=False)
    training_end = db.Column(db.DateTime, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.String, nullable=False)  # String으로 정의
    role_target = db.Column(db.String, nullable=False)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_finished = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(TrainingStatus), default=TrainingStatus.PLAN, nullable=False)

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)



    @validates('dept_target', 'role_target')
    def validate_targets(self, key, value):
        if isinstance(value, list):
            return ','.join(value)
        return value


    def update_status(self):
        now = datetime.utcnow()
        if self.training_start <= now <= self.training_end:
            self.status = TrainingStatus.RUN
        elif now > self.training_end:
            self.status = TrainingStatus.FIN


    def to_dict(self):
        # Get base fields
        data = self.base_to_dict()
        
        data['dept_target'] = self.dept_target.split(',') if self.dept_target else []
        data['role_target'] = self.role_target.split(',') if self.role_target else []

        return data


    @staticmethod
    def required_fields():
        return ['training_name', 'training_desc', 'training_start', 'training_end', 'resource_user'
                ,'max_phishing_mail','dept_target','role_target']
        
    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value
            
    def __init__(self, **kwargs):
        # Ensure lists are stored as comma-separated strings
        if 'dept_target' in kwargs and isinstance(kwargs['dept_target'], list):
            kwargs['dept_target'] = ','.join(kwargs['dept_target'])
        if 'role_target' in kwargs and isinstance(kwargs['role_target'], list):
            kwargs['role_target'] = ','.join(kwargs['role_target'])
        super(Training, self).__init__(**kwargs)