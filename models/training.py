from sqlalchemy.types import TypeDecorator, TEXT
import json
from extensions import db
from datetime import datetime
from models.base_model import BaseModel
from enum import Enum
from sqlalchemy.orm import validates
 
class TrainingStatus(Enum):
    PLAN = "PLAN"
    RUN = "RUN"
    FIN = "FIN"


class JSONEncodedList(TypeDecorator):
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value
    
class Training(BaseModel):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.DateTime, nullable=False)
    training_end = db.Column(db.DateTime, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(JSONEncodedList, nullable=False)
 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_finished = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(TrainingStatus), default=TrainingStatus.PLAN, nullable=False)

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('Department', back_populates='trainings')