from extensions import db
from datetime import datetime
from models.serializable_mixin import SerializableMixin
from models.base_model import BaseModel

class Email(BaseModel, SerializableMixin):
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_phishing = db.Column(db.Boolean, default=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    employee = db.relationship('Employee', backref='emails', lazy=True)

    training_id = db.Column(db.Integer,db.ForeignKey('trainings.id'),nullable=True)
    completed_training_id = db.Column(db.Integer, db.ForeignKey('complete_trainings.id'), nullable=True)

    department_name  = db.Column(db.String(100), db.ForeignKey('departments.name'), nullable=True)
    department = db.relationship('Department', backref='emails', lazy=True,foreign_keys=[department_name])

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'body': self.body,
            'sender': self.sender,
            'recipient': self.recipient,
            'sent_date': self.sent_date.strftime('%Y-%m-%d %H:%M:%S') if self.sent_date else None,
            'is_phishing': self.is_phishing,
            'employee_id': self.employee_id,
            'training_id' :self.training_id,
            'complete_training' : self.completed_training_id
        }
    
    def __repr__(self):
        return f'<Email {self.subject}>'
    

    @staticmethod
    def required_fields():
        return ['subject', 'body', 'sender', 'recipient', 'sent_date']

    @staticmethod
    def parse_datetime(value):
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        return value