from sqlalchemy.types import TypeDecorator, TEXT
import json
from extensions import db
from datetime import datetime
from models.base_model import BaseModel
from enum import Enum
from sqlalchemy.orm import validates
class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"
    
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value

class CompleteTraining(BaseModel):
    __tablename__ = 'complete_trainings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_id = db.Column(db.Integer, nullable=False)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.DateTime, nullable=False)
    training_end = db.Column(db.DateTime, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(JSONEncodedDict, nullable=False)
    status = db.Column(db.Enum(TrainingStatus), default=TrainingStatus.FIN, nullable=False)

    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관련 이메일 관리
    emails = db.relationship('Email', backref='complete_training', lazy=True)

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
    
 