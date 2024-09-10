from extensions import db

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code1 = db.Column(db.String(10), nullable=False)
    code2 = db.Column(db.String(50), nullable=False)
    korean_name = db.Column(db.String(100), nullable=False)

    employees = db.relationship('Employee', back_populates='department')

    def __repr__(self):
        return f'<Department {self.name}>'