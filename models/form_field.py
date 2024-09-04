from extensions import db

class FormField(db.Model):
    __tablename__ = 'form_fields'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)
    is_required = db.Column(db.Boolean, default=False)

    form = db.relationship('Form', back_populates='form_fields')

class FormFieldResponse(db.Model):
    __tablename__ = 'form_field_responses'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('form_submissions.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('form_fields.id'), nullable=False)
    field_value = db.Column(db.Text)

    submission = db.relationship('FormSubmission', back_populates='responses')
    field = db.relationship('FormField')