from extensions import db
from datetime import datetime
from models.training import Training
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin

class DeletedTraining(BaseModel, SerializableMixin):
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
    is_Reported = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255), nullable=True)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(DeletedTraining, self).__init__(**kwargs)

    def to_dict(self):
        # 기본적으로 상위 클래스의 to_dict 호출
        data = super().to_dict()

        # dept_target과 role_target을 리스트로 변환
        data['dept_target'] = self.dept_target.split(',') if self.dept_target else []
        data['role_target'] = self.role_target.split(',') if self.role_target else []

        # DateTime 필드를 "YYYY-MM-DD HH:MM:SS" 형식으로 변환
        date_format = "%Y-%m-%d %H:%M:%S"
        data['created_at'] = self.created_at.strftime(date_format) if self.created_at else None
        data['deleted_at'] = self.deleted_at.strftime(date_format) if self.deleted_at else None
        data['training_start'] = self.training_start.strftime(date_format) if self.training_start else None
        data['training_end'] = self.training_end.strftime(date_format) if self.training_end else None

        return data
