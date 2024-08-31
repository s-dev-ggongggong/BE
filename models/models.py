from marshmallow import fields
from extensions import db, ma

class AuthToken(db.Model):
    __tablename__ = 'authtoken'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(256), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User

    user = db.relationship('User', backref=db.backref('auth_tokens', lazy=True))

    def __repr__(self):
        return f'<AuthToken {self.token}>'

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Url {self.url}>'

# Schema definitions

