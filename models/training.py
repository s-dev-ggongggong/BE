from extensions import db
from datetime import datetime
import json
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin

class Training(BaseModel,SerializableMixin):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    training_desc = db.Column(db.Text, nullable=False)
    training_start = db.Column(db.Date, nullable=False)
    training_end = db.Column(db.Date, nullable=False)
    resource_user = db.Column(db.Integer, nullable=False)
    max_phishing_mail = db.Column(db.Integer, nullable=False)
    dept_target = db.Column(db.String, nullable=False)  # String으로 정의
    role_target = db.Column(db.String, nullable=False)  

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_finished = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255),nullable=True)





    def __init__(self, **kwargs):
        if 'dept_target' in kwargs and isinstance(kwargs['dept_target'], list):
            kwargs['dept_target'] = ','.join(kwargs['dept_target'])
        if 'role_target' in kwargs and isinstance(kwargs['role_target'], list):
            kwargs['role_target'] = ','.join(kwargs['role_target'])
        super(Training, self).__init__(**kwargs)


    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['deptTarget'] = self.dept_target.split(',') if self.dept_target else []
        data['roleTarget'] = self.role_target.split(',') if self.role_target else []
        #return {k: v for k, v in data.items() if v not in [None, '']}
        return data

  
    def __repr__(self):
        return f'<Training {self.training_name}>'
    

    @staticmethod
    def required_fields():
        return ['training_name', 'training_desc', 'training_start', 'training_end', 'resource_user'
                ,'max_phishing_mail','dept_target','role_target']
        