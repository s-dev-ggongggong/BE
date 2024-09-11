from extensions import db
from datetime import datetime
from models.serializable_mixin import SerializableMixin
class Email(db.Model, SerializableMixin):
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_phishing = db.Column(db.Boolean, default=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)

    training_id = db.Column(db.Integer,db.ForeignKey('trainings.id'),nullable=True)
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'body': self.body,
            'sender': self.sender,
            'recipient': self.recipient,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None,
            'is_phishing': self.is_phishing,
            'employee_id': self.employee_id,
            'training_id' :self.training_id
        }
    
    def __repr__(self):
        return f'<Email {self.subject}>'
