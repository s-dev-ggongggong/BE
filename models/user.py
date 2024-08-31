from extensions import db,ma
from marshmallow import fields

class User(db.Model):

    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
 
    def __init__(self,username,email,password_hash):
        self.username= username
        self.email=email
        self.password_hash =password_hash
    
    def __repr__(self):
        return '<User %r>' % self.username

