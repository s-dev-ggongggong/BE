from extensions import db
from models.serializable_mixin import SerializableMixin
from models.base_model import BaseModel

class Employee(BaseModel,SerializableMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
     # Foreign keys for Role and Department
    role_name = db.Column(db.String(50), db.ForeignKey('roles.name'), nullable=False)
    department_name = db.Column(db.String(100), db.ForeignKey('departments.name'), nullable=False)
    admin_id = db.Column(db.String(50), unique=True, nullable=True)
    admin_pw = db.Column(db.String(50), unique=True, nullable=True)

    # Relationships to the Role and Department models
    role = db.relationship('Role', back_populates='employees')
    department = db.relationship('Department', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role_name': self.role_name.isoformat() if self.role_name else None,
            'department_name': self.department_name.isoformat() if self.department_name else None,
            'role': self.role,
            'department':self.department
        }
    
    
    @staticmethod
    def required_fields():
        return ['name', 'email', 'password', 'role_name', 'department_name']