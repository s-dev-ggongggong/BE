from extensions import db
from datetime import datetime
import json

class Training(db.Model):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.Date, nullable=False)
    training_end = db.Column(db.Date, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.String(255), nullable=False) 
    role_target = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_finished = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255),nullable=True)

    def get_dept_target(self):
        return json.loads(self.dept_target)

    def get_role_target(self):
        return json.loads(self.role_target)

    def set_dept_target(self, target_list):
        self.dept_target = json.dumps(target_list)

    def set_role_target(self, target_list):
        self.role_target = json.dumps(target_list)

    def __repr__(self):
        return f'<Training {self.training_name}>'