from extensions import db

class Form(db.Model):
    __tablename__ = 'forms'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)  # Added description field

    creator = db.relationship('Employee', foreign_keys=[creator_id], back_populates='created_forms')
    form_fields = db.relationship('FormField', back_populates='form')
    submissions = db.relationship('FormSubmission', back_populates='form')

class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    form = db.relationship('Form', back_populates='submissions')
    employee = db.relationship('Employee', back_populates='form_submissions')
    responses = db.relationship('FormFieldResponse', back_populates='submission')