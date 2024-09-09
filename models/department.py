# models/department.py

from extensions import db

class Department(db.Model):
    __tablename__ = 'departments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    employees = db.relationship('Employee', back_populates='department')

    def __repr__(self):
        return f'<Department {self.name}>'
