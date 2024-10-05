from extensions import db
from models.base_model import BaseModel
from models.serializable_mixin import SerializableMixin
class Department(BaseModel,SerializableMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code1 = db.Column(db.String(10), nullable=False)
    code2 = db.Column(db.String(50), nullable=False)
    korean_name = db.Column(db.String(100), nullable=False)
    
    complete_trainings = db.relationship(
        'CompleteTraining',
        secondary='complete_training_department',
        back_populates='departments'
    )
     
    employees = db.relationship('Employee', back_populates='department')
    trainings = db.relationship('Training', secondary='training_department', back_populates='departments')
    complete_trainings = db.relationship('CompleteTraining', secondary='complete_training_department', back_populates='departments')


 # 리스트를 문자열로 저장

    def __repr__(self):
        return f'<Department {self.name}>'
    
    def to_dict(self):  
        return {
            'id': self.id,
            'name': self.name,
            'code1': self.code1,
            'code2': self.code2,
            'korean_name': self.korean_name,  # korean_name is a string, no isoformat() needed
            'employees': [emp.id for emp in self.employees],  # Returning a list of employee IDs
            
        }
    
    @staticmethod
    def required_fields():
        return ['name', 'code1', 'code2', 'korean_name']
