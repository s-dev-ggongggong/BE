    from sqlalchemy.orm import validates
    from extensions import db
    from models.base_model import BaseModel
    import json

    class EventLog(BaseModel):
        __tablename__ = 'event_logs'
        
        id = db.Column(db.Integer, primary_key=True)
        action = db.Column(db.String(50), nullable=False)
        timestamp = db.Column(db.DateTime, nullable=False)
        training_id = db.Column(db.Integer)
        department_id = db.Column(db.Integer)
        employee_id = db.Column(db.String(255))
        email_id = db.Column(db.String(255))
        role_id = db.Column(db.Integer)
        data = db.Column(db.JSON)

        @validates('action')
        def validate_action(self, key, action):
            allowed_actions = [ 'remove', 'targetSetting']
            assert action in allowed_actions, f"Invalid action: {action}"
            return action
        def set_data(self, data_dict):
            self.data = data_dict

        @classmethod
        def required_fields(cls):
            return ['action', 'timestamp', 'training_id', 'data']