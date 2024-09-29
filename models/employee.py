from extensions import db
from models.serializable_mixin import SerializableMixin
from models.base_model import BaseModel

class Employee(BaseModel,SerializableMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password= db.Column(db.String(100),default='igloo1234',nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
     
    role = db.relationship('Role', back_populates='employees')
    department = db.relationship('Department', back_populates='employees')


    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        return data
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
        
 