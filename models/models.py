from marshmallow import fields
from extensions import db, ma
from models.employee import Employee


# class Form(db.Model):
#     __tablename__ = 'forms'
#     id = db.Column(db.Integer, primary_key=True)
#     creator_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    
#     creator = db.relationship('Employee', foreign_keys=[creator_id], back_populates='created_forms')
    
#     form_fields = db.relationship('FormField', back_populates='form')

# class FormField(db.Model):    
#     __tablename__ = 'form_field' 
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)     
#     form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
#     field_name = db.Column(db.String(120), nullable=False)
#     field_type = db.Column(db.String(50), nullable=False)
    
#     form = db.relationship('Form', back_populates='form_fields')
#     responses = db.relationship('FormFieldResponse', back_populates='form_field')

#     def __repr__(self):         
#         return f'<FormField {self.field_name} ({self.field_type})>'
# class FormSubmission(db.Model):
#     __tablename__ = 'form_submissions'
#     id = db.Column(db.Integer, primary_key=True)
#     form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

#     form = db.relationship('Form', back_populates='submissions')
#     employee = db.relationship('Employee', back_populates='form_submissions')
#     responses = db.relationship('FormFieldResponse', back_populates='submission')


# class FormFieldResponse(db.Model):
#     __tablename__ = 'form_field_responses'
    
#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
#     form_field_id = db.Column(db.Integer, db.ForeignKey('form_field.id'), nullable=False)
#     response = db.Column(db.Text, nullable=True)

#     employee = db.relationship('Employee', back_populates='form_field_responses')
#     form_field = db.relationship('FormField', back_populates='responses')