from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLAlchemyEnum
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

class UserEventLog(db.Model):
    __tablename__ = 'user_event_logs'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)    
    training_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    email_id = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    data = db.Column(db.Text)