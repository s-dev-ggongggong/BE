from extensions import db, ma
from marshmallow import fields,validate
from datetime import datetime, date
import random

class Training(db.Model):
    __tablename__ = 'trainings'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    trainingName = db.Column(db.String(100), nullable=False)
    trainingDesc = db.Column(db.Text, nullable=False)
    trainingStart = db.Column(db.Date, nullable=False)
    trainingEnd = db.Column(db.Date, nullable=False)
    resourceUser = db.Column(db.Integer, nullable=False)
    maxPhishingMail = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    agentStartDate = db.Column(db.Date, nullable=True)
    department = db.Column(db.String(50), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    agentId = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    agent = db.relationship('Agent', back_populates='trainings', lazy=True)
    user = db.relationship('User', back_populates='trainings', lazy='select')


    
    def __init__(self, trainingName, trainingDesc, trainingStart, trainingEnd,
                 resourceUser, maxPhishingMail, status, department, userId=None,
                 agentStartDate=None, agentId=None):
                 
        self.trainingName = trainingName
        self.trainingDesc = trainingDesc
        self.trainingStart = self._parse_date(trainingStart)
        self.trainingEnd = self._parse_date(trainingEnd)
        self.resourceUser = resourceUser
        self.maxPhishingMail = maxPhishingMail
        self.set_status(status)
        self.department = department
        self.agentStartDate = self._parse_date(agentStartDate) if agentStartDate else None
        self.agentId = agentId
        self.userId = userId
    @staticmethod
    def _parse_date(date_value):
        if isinstance(date_value, date):
            return date_value
        elif isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        else:
            raise ValueError("Invalid date format. Expected datetime.date or string in format 'YYYY-MM-DD'")


    def set_status(self, status):
        valid_statuses = ['pending', 'in_progress', 'completed']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'trainingName': self.trainingName,
            'trainingDesc': self.trainingDesc,
            'trainingStart': self.trainingStart.isoformat(),
            'trainingEnd': self.trainingEnd.isoformat(),
            'resourceUser': self.resourceUser,
            'maxPhishingMail': self.maxPhishingMail,
            'status': self.status,
            'department': self.department,
            'agentStartDate': self.agentStartDate.isoformat() if self.agentStartDate else None,
            'createdAt': self.createdAt.isoformat(),
            'updatedAt': self.updatedAt.isoformat(),
            'agentId': self.agentId,
             'userId':self.userId
        }