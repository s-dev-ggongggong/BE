from extensions import db
from datetime import datetime
from models.serializable_mixin import SerializableMixin
from models.base_model import BaseModel

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
    dept_target = db.Column(db.String(255), nullable=False)
    role_target = db.Column(db.String(255), nullable=False)
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
            'dept_target': self.dept_target.split(',') if self.dept_target else [],
            'role_target': self.role_target.split(',') if self.role_target else [],
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None,
            'emails': [email.to_dict() for email in self.emails]  # Assuming Email has a to_dict method
            }
    

    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value

    def __repr__(self):
        return f'<CompleteTraining {self.training_name}>'