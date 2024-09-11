from extensions import db
from models.serializable_mixin import SerializableMixin
class Role(db.Model,SerializableMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    korean_name = db.Column(db.String(50), nullable=False)

    employees = db.relationship('Employee', back_populates='role')

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'korean_name': self.korean_name,
            'employees': self.employees

        }

    def __repr__(self):
        return f'<Role {self.name}>'