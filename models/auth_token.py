from extensions import db
 
from extensions import db

class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)  # 추가
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    
    def __repr__(self):
        return f'<AuthToken {self.token}>'
