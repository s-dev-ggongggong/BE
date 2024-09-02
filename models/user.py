from extensions import db,ma
from marshmallow import fields 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__='users'
    __table_args__ = {'extend_existing':True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    
    trainings = db.relationship('Training', back_populates='user', lazy='dynamic')
    def __init__(self,username,email,password):
        self.username= username
        self.email=email
        self.set_password(password) 
    
    def set_password(self,password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.passwordHash,password)
    
    def __repr__(self):
        return '<User %r>' % self.username

