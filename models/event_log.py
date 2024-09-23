from extensions import db
from datetime import datetime
import json
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin

class EventLog(BaseModel, SerializableMixin):
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    training_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    email_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)

    # 추가 데이터를 JSON 형태로 저장
    data = db.Column(db.Text)

    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)

    def get_data(self):
        return json.loads(self.data) if self.data else {}

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.get_data()
        return result
    
    @staticmethod
    def required_fields():
        return ['action', 'timestamp', 'training_id', 'message']
