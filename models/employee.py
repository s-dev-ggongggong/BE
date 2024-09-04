from extensions import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class Employee(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    department = db.relationship('Department', back_populates='employees')
    role = db.relationship('Role', back_populates='employees')
    event_logs = db.relationship('EventLog', back_populates='employee', lazy='dynamic')
    trainings = db.relationship('Training', back_populates='employee', lazy='dynamic')
    auth_tokens = db.relationship("AuthToken", back_populates="employee_auth", lazy=True)
    created_forms = db.relationship('Form', foreign_keys='Form.creator_id', back_populates='creator')
    form_submissions = db.relationship('FormSubmission', back_populates='employee')
 
    def __init__(self, username, email, password, department_id, role_id):
        self.username = username
        self.email = email
        self.department_id = department_id
        self.role_id = role_id
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Employee {self.username}>'



