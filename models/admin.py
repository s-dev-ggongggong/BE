from extensions import db

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
