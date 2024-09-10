from extensions import db

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
 
     # Foreign keys for Role and Department
    role_name = db.Column(db.String(50), db.ForeignKey('roles.name'), nullable=False)
    department_name = db.Column(db.String(100), db.ForeignKey('departments.name'), nullable=False)

    # Relationships to the Role and Department models
    role = db.relationship('Role', back_populates='employees')
    department = db.relationship('Department', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.name}>'