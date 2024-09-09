from extensions import db
from datetime import datetime

class AuthToken(db.Model):
    __tablename__ = 'auth_token'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    token = db.Column(db.String(256), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)

    employee_auth = db.relationship('Employee', back_populates='auth_tokens')  # Updated relationship

    def __repr__(self):
        return f'<AuthToken {self.token}>'
