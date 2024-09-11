from extensions import db
 
from extensions import db
from models.serializable_mixin import SerializableMixin
class AuthToken(db.Model,SerializableMixin):
    __tablename__ = 'auth_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)  # 추가
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    
    def __repr__(self):
        return f'<AuthToken {self.token}>'
   
    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'employee_id': self.employee_id.isoformat() if self.employee_id else None
        }