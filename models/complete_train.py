from sqlalchemy.types import TypeDecorator, TEXT
import json
from extensions import db
from datetime import datetime
from models.base_model import BaseModel
from enum import Enum
from sqlalchemy.orm import validates
   
from sqlalchemy.types import TypeDecorator, VARCHAR
import json


class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"



class JSONEncodedList(TypeDecorator):
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value else '[]'

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else []



complete_training_department = db.Table('complete_training_department',
    db.Column('complete_training_id', db.Integer, db.ForeignKey('complete_trainings.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id'), primary_key=True)
)

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
class CompleteTraining(BaseModel):
    __tablename__ = 'complete_trainings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.DateTime, nullable=False)
    training_end = db.Column(db.DateTime, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.Text, nullable=False)
    
    departments = db.relationship(
        'Department',
        secondary='complete_training_department',
        back_populates='complete_trainings'
    )    
    status = db.Column(db.Enum(TrainingStatus), default=TrainingStatus.FIN, nullable=False)

    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    original_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    original_training = db.relationship('Training', back_populates='complete_training', foreign_keys=[original_id])
    
    # 관련 이메일 관리
    emails = db.relationship('Email', backref='complete_training', lazy=True)

    @property
    def dept_target_list(self):
        try:
            return [int(x) for x in json.loads(self.dept_target)]
        except (json.JSONDecodeError, ValueError, TypeError):
            return []

    @dept_target_list.setter
    def dept_target_list(self, value):
        self.dept_target = json.dumps([str(x) for x in value])
   

    def to_dict(self):
        return {
            'id': self.id,
            'original_id': self.original_id,
            'training_name': self.training_name,
            'training_desc': self.training_desc,
            'training_start': self.training_start.strftime('%Y-%m-%d %H:%M:%S') if self.training_start else None,
            'training_end': self.training_end.strftime('%Y-%m-%d %H:%M:%S') if self.training_end else None,
            'resource_user': self.resource_user,
            'max_phishing_mail': self.max_phishing_mail,
            'dept_target': self.dept_target, 
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None,
            'emails': [email.to_dict() for email in self.emails]  # Assuming Email has a to_dict method
            }
    
 