from extensions import db
from datetime import datetime

class EventLog(db.Model):
    __tablename__ = 'event_logs'  # Updated to plural for consistency
    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  # Link to Employee
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)  # Link to Department if needed
    position = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    training = db.relationship('Training', back_populates='event_logs')
    employee = db.relationship('Employee', back_populates='event_logs')
    department = db.relationship('Department')  # Assuming you have a Department model

    def __init__(self, training_id, employee_id, department_id, position, email, name, action):
        self.training_id = training_id
        self.employee_id = employee_id
        self.department_id = department_id
        self.position = position
        self.email = email
        self.name = name
        self.action = action
