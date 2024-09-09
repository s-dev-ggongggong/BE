from extensions import db, ma
from marshmallow import fields,validate
from datetime import datetime, date
import random

class Training(db.Model):
    __tablename__ = 'trainings'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    training_name = db.Column(db.String(100), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.Date, nullable=False)
    training_end = db.Column(db.Date, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    agent_startDate = db.Column(db.Date, nullable=True)
    department = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
   
    agent = db.relationship('Agent', back_populates='trainings', lazy=True)
    employee = db.relationship('Employee', back_populates='trainings', lazy='select')
    event_logs = db.relationship('EventLog', back_populates='training', lazy='dynamic')

    def __init__(self, training_name, training_desc, training_start, training_end,
                 resource_user, max_phishing_mail, status, department, employee_id=None,
                 agent_startDate=None, agent_id=None):
                 
        self.training_name = training_name
        self.training_desc = training_desc
        self.training_start = self._parse_date(training_start)
        self.training_end = self._parse_date(training_end)
        self.resource_user = resource_user
        self.max_phishing_mail = max_phishing_mail
        self.set_status(status)
        self.department = department
        self.agent_startDate = self._parse_date(agent_startDate) if agent_startDate else None
        self.agent_id = agent_id
        self.employee_id = employee_id

    @staticmethod
    def _parse_date(date_value):
        if isinstance(date_value, date):
            return date_value
        elif isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        else:
            raise ValueError("Invalid date format. Expected datetime.date or string in format 'YYYY-MM-DD'")


    def set_status(self, status):
        valid_statuses = ['PLAN', 'RUN', 'FIN']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'training_name': self.training_name,
            'training_desc': self.training_desc,
            'training_start': self.training_start.isoformat(),
            'training_end': self.training_end.isoformat(),
            'resource_user': self.resource_user,
            'max_phishing_mail': self.max_phishing_mail,
            'status': self.status,
            'department': self.department,
            'agent_startDate': self.agent_startDate.isoformat() if self.agent_startDate else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'agent_id': self.agent_id,
            'employee_id': self.employee_id}