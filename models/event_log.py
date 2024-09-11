from extensions import db
from datetime import datetime
import json
from models.serializable_mixin import SerializableMixin
class EventLog(db.Model, SerializableMixin):
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 관련 엔티티의 ID를 저장. 필요에 따라 Null 허용
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

    def __repr__(self):
        return f'<EventLog {self.action} - {self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp,
            'training_id': self.training_id,
            'employee_id': self.employee_id.isoformat() if self.employee_id else None,
            'email_id': self.email_id.isoformat() if self.email_id else None,
            'role_id': self.role_id,
        }