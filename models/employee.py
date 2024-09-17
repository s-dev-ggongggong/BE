from extensions import db
from models.serializable_mixin import SerializableMixin
from models.base_model import BaseModel

class Employee(BaseModel,SerializableMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    role_name = db.Column(db.String(50), db.ForeignKey('roles.name'), nullable=False)
    department_name = db.Column(db.String(100), db.ForeignKey('departments.name'), nullable=False)

    admin_id = db.Column(db.String(50), nullable=True)
    admin_pw = db.Column(db.String(50), nullable=True)

    role = db.relationship('Role', back_populates='employees')
    department = db.relationship('Department', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'admin_id': self.admin_id,
            'admin_pw': self.admin_pw
        })
        return data
    
        
    
    @staticmethod
    def required_fields():
        return ['name', 'email', 'password', 'role_name', 'department_name']