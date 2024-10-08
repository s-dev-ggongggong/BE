from extensions import db

from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin
class Role(BaseModel,SerializableMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    korean_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)

    employees = db.relationship('Employee', back_populates='role')

    
    def to_dict(self):
        data = self.base_to_dict()  # Get base fields
        # Add or modify specific fields
        data['custom_field'] = 'custom_value'
        return data
    def __repr__(self):
        return f'<Role {self.name}>'
    

    @staticmethod
    def required_fields():
        return ['korean_name','name']