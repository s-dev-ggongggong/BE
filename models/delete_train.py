from extensions import db
from datetime import datetime
import json
from models.training import Training
from models.serializable_mixin import SerializableMixin
class DeletedTraining(db.Model, SerializableMixin):
    __tablename__ = 'deleted_trainings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_id = db.Column(db.Integer)
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
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self, **kwargs):
        super(DeletedTraining, self).__init__(**kwargs)


    def to_dict(self):
        data = super().to_dict()
        data['dept_target'] = self.dept_target.split(',') if self.dept_target else []
        data['role_target'] = self.role_target.split(',') if self.role_target else []
        return data
        