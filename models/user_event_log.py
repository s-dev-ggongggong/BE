from extensions import db
from datetime import datetime, timedelta
import json
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin

class UserEventLog(BaseModel, SerializableMixin):
    __tablename__ = 'user_event_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    department_name = db.Column(db.String(255), nullable=False)
    phishing_link = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # 'link_generated', 'link_clicked' 등 이벤트 유형
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=9))  # 한국 표준시(KST) 설정
    data = db.Column(db.Text, nullable=True)  # 추가 데이터를 JSON으로 저장

    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)

    def get_data(self):
        return json.loads(self.data) if self.data else {}

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.get_data() or {}  # 데이터가 없는 경우 빈 사전 반환
        return result
