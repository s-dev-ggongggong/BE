from extensions import db
from models.serializable_mixin import SerializableMixin
class Department(db.Model,SerializableMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code1 = db.Column(db.String(10), nullable=False)
    code2 = db.Column(db.String(50), nullable=False)
    korean_name = db.Column(db.String(100), nullable=False)

    employees = db.relationship('Employee', back_populates='department')
    dept_target = db.Column(db.String(255))  # 리스트를 문자열로 저장

    def __repr__(self):
        return f'<Department {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code1': self.code1,
            'code2': self.code2,
            'korean_name': self.korean_name.isoformat() if self.korean_name else None,
            'employees': self.employees.isoformat() if self.employees else None,
            'dept_target': self.dept_target.split(',') if self.dept_target else []
        
        }