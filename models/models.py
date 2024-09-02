from marshmallow import fields
from extensions import db, ma

class AuthToken(db.Model):
    __tablename__ = 'authtoken'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(256), nullable=False, unique=True)
    createdAt = db.Column(db.DateTime, default=db.func.now())
    expiresAt = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User

    user = db.relationship('User', backref=db.backref('auth_tokens', lazy=True))

    def __repr__(self):
        return f'<AuthToken {self.token}>'

class Form(db.Model):
    __tablename__ = 'form'
    __table_args__={'extend_existing':True}
    
    id = db.Column(db.Integer, primary_key=True)
    formName = db.Column(db.String(120), nullable=False)
    fields = db.relationship('FormField', backref='form', lazy=True)

class FormField(db.Model):
    __tablename__ = 'form_field'
    __table_args__={'extend_existing':True}

    id = db.Column(db.Integer, primary_key=True)
    formId = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    fieldName = db.Column(db.String(120), nullable=False)
    fieldType = db.Column(db.String(50), nullable=False)  # 예: 'text', 'checkbox', 'radio'

    def __repr__(self):
        return f'<FormField {self.field_name} ({self.field_type})>'

class Url(db.Model):
    __tablename__ = 'url'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Url {self.url}>'

# Schema definitions

