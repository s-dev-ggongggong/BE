from extensions import db
from datetime import datetime
import json
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin
from enum import Enum

class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"
class Training(BaseModel):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.Date, nullable=False)
    training_end = db.Column(db.Date, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.String, nullable=False)  # String으로 정의
    role_target = db.Column(db.String, nullable=False)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_finished = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(TrainingStatus), default=TrainingStatus.PLAN, nullable=False)


    def update_status(self):
        now = datetime.utcnow().date()
        if self.training_start <= now <= self.training_end:
            self.status = TrainingStatus.RUN
        elif now > self.training_end:
            self.status = TrainingStatus.FIN




    def __init__(self, **kwargs):
        if 'dept_target' in kwargs and isinstance(kwargs['dept_target'], list):
            kwargs['dept_target'] = ','.join(kwargs['dept_target'])
        if 'role_target' in kwargs and isinstance(kwargs['role_target'], list):
            kwargs['role_target'] = ','.join(kwargs['role_target'])
        super(Training, self).__init__(**kwargs)


    def to_dict(self):
        return {
            'id': self.id,
            'training_name': self.training_name,
            'training_desc': self.training_desc,
            'status': self.status.name if hasattr(self.status, 'name') else self.status,  # Convert enum to string
            'training_start': self.training_start.strftime('%Y-%m-%d %H:%M:%S') if self.training_start else None,
            'training_end': self.training_end.strftime('%Y-%m-%d %H:%M:%S') if self.training_end else None,
            'resource_user': self.resource_user,
            'max_phishing_mail': self.max_phishing_mail,
            'dept_target': self.dept_target if isinstance(self.dept_target, list) else [],  # Ensure list
            'role_target': self.role_target if isinstance(self.role_target, list) else [],  # Ensure list
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'is_finished': self.is_finished
         }

  
    def __repr__(self):
        return f'<Training {self.training_name}>'
    

    @staticmethod
    def required_fields():
        return ['training_name', 'training_desc', 'training_start', 'training_end', 'resource_user'
                ,'max_phishing_mail','dept_target','role_target']
        