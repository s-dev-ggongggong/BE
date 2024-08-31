from extensions import db, ma
from marshmallow import fields

class Email(db.Model):
    __tablename__='emails'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    sent_date = db.Column(db.DateTime, nullable=False)
