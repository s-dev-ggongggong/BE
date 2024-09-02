from extensions import db, ma
from marshmallow import fields

class Email(db.Model):
    __tablename__='emails'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    sentDate = db.Column(db.DateTime, nullable=False)
class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    receivedDate = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, sender, subject, body):
        self.sender = sender
        self.subject = subject
        self.body = body

    def __repr__(self):
        return f"<EmailLog from={self.sender} subject={self.subject}>"