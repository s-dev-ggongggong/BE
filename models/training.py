from sqlalchemy.types import TypeDecorator, TEXT
import json
from extensions import db
from datetime import datetime
from models.base_model import BaseModel
from enum import Enum
from sqlalchemy.orm import validates
from marshmallow import fields, pre_load, post_dump, ValidationError
from marshmallow_enum import EnumField


from marshmallow import fields, ValidationError
from datetime import datetime

class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"

training_department = db.Table('training_department',
    db.Column('training_id', db.Integer, db.ForeignKey('trainings.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id'), primary_key=True)
)


class Training(BaseModel):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.DateTime, nullable=False)
    training_end = db.Column(db.DateTime, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.Text, nullable=False, default='[]')


    departments = db.relationship('Department', secondary='training_department', back_populates='trainings')
 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_finished = db.Column(db.Boolean, default=False)
    status = EnumField(TrainingStatus, by_value=True)

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)


    complete_training = db.relationship('CompleteTraining', uselist=False, back_populates='original_training')
    event_logs = db.relationship('EventLog', back_populates='training')



   
    @property
    def dept_target_list(self):
        try:
            return json.loads(self.dept_target)
        except json.JSONDecodeError:
            return []

    @dept_target_list.setter
    def dept_target_list(self, value):
        self.dept_target = json.dumps(value)