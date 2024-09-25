from flask import json
from marshmallow import fields, post_load, validates, ValidationError,validates_schema, pre_load, post_dump
from sqlalchemy import or_
from extensions import ma, db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.department import Department
from models.role import Role
from models.employee import Employee
from models.training import Training
from models.email import Email
from models.complete_train import CompleteTraining
from models.event_log import EventLog
 
# Base Schema
class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session

# Define schemas with data_key for camelCaseem
class DepartmentSchema(Base):
    id = fields.Int(data_key="id",dump_only=True)
    name = fields.Str(data_key="name")
    code1 = fields.Str(data_key="code1")
    code2 = fields.Str(data_key="code2")
    korean_name = fields.Str(data_key="koreanName")
    description = fields.Str(data_key="description")
    dept_target = fields.List(fields.Str(), data_key="deptTarget")


    @pre_load
    def process_targets(self, data, **kwargs):
        if 'deptTarget' in data and isinstance(data['deptTarget'], list):
            data['dept_target'] = ','.join(data['deptTarget'])
        return data

    @post_dump
    def process_targets_dump(self, data, **kwargs):
        if 'dept_target' in data and isinstance(data['dept_target'], str):
            data['deptTarget'] = data['dept_target'].split(',')
        return data
    
    class Meta(Base.Meta):
        model = Department

class RoleSchema(Base):
        id = fields.Int(data_key="id",dump_only=True)
        name = fields.Str(data_key="name",dump_only=True)
        korean_name = fields.Str(data_key="koreanName")
        class Meta(Base.Meta):
            model = Role

class EmployeeSchema(Base):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)
    department_id = fields.Int(required=True)
    is_admin = fields.Boolean(dump_only=True)

    role = fields.Nested(RoleSchema, only=('id', 'name'))
    department = fields.Nested(DepartmentSchema, only=('id', 'name'))

    class Meta(Base.Meta):
        model = Employee
        exclude = ('password',)
        

    @validates('role_id')
    def validate_role(self, value):
        role = Role.query.get(value)
        if not role:
            raise ValidationError('Invalid role ID.')

    @validates('department_id')
    def validate_department(self, value):
        department = Department.query.get(value)
        if not department:
            raise ValidationError('Invalid department ID.')
            
class TrainingSchema(Base):
    id = fields.Int(dump_only=True)
    training_name = fields.Str(data_key="trainingName")
    training_desc = fields.Str(data_key="trainingDesc")
    training_start = fields.DateTime(data_key="trainingStart", format='iso', load_format='iso')
    training_end = fields.DateTime(data_key="trainingEnd", format='iso', load_format='iso')
    resource_user = fields.Int(data_key="resourceUser")
    max_phishing_mail = fields.Int(data_key="maxPhishingMail")
    dept_target = fields.List(fields.Integer(), data_key='departTarget', required=True)
    
    created_at = fields.DateTime(dump_only=True, format='iso')
    is_finished = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True, format='iso', load_format='iso')
    

    @pre_load
    def process_input(self, data, **kwargs):
        if 'deptTarget' in data and isinstance(data['deptTarget'], str):
            data['deptTarget'] = json.loads(data['deptTarget'])
        return data

    @post_dump
    def process_output(self, data, **kwargs):
        if 'dept_target' in data:
            data['deptTarget'] = data['dept_target']
            del data['dept_target']
        return data
    
class Meta(Base.Meta):
        model = Training

class EventLogSchema(Base):
    id = fields.Int(data_key="id")
    action = fields.Str(data_key="action")
    timestamp = fields.DateTime(data_key="timestamp", format='iso', load_format='iso', dump_format='%Y-%m-%d %H:%M:%S')
    training_id = fields.Int(data_key="trainingId")
    department_id = fields.Int(data_key="departmentId")
    data = fields.Dict(data_key="data")

    @pre_load
    def process_department_id(self, data, **kwargs):
        if 'departmentId' in data and isinstance(data['departmentId'], list):
            data['department_id'] = json.dumps(data['departmentId'])
        return data

    
    @post_dump
    def process_department_id_dump(self, data, **kwargs):
        if 'department_id' in data and isinstance(data['department_id'], str):
            try:
                data['departmentId'] = json.loads(data['department_id'])
                del data['department_id']
            except json.JSONDecodeError:
                data['departmentId'] = []
        return data
    

    class Meta(Base.Meta):
        model = EventLog
    
 
 

class CompleteTrainingSchema(Base):
    id = fields.Int(dump_only=True)
    original_id = fields.Int(required=True)
    completed_at = fields.DateTime(dump_only=True, format='iso', load_format='iso', dump_format='%Y-%m-%d %H:%M:%S')
    
    training_name = fields.Str(data_key="trainingName")
    training_desc = fields.Str(data_key="trainingDesc")
    training_start = fields.DateTime(data_key="trainingStart", format='iso', load_format='iso')
    training_end = fields.DateTime(data_key="trainingEnd", format='iso', load_format='iso')
    resource_user = fields.Int(data_key="resourceUser")
    max_phishing_mail = fields.Int(data_key="maxPhishingMail")
    dept_target = fields.List(fields.Integer(), data_key='departTarget', required=True)

    @pre_load
    def process_input(self, data, **kwargs):
        if 'departTarget' in data and isinstance(data['departTarget'], str):
            data['departTarget'] = json.loads(data['departTarget'])
        return data

    @post_dump
    def process_output(self, data, **kwargs):
        if 'dept_target' in data:
            data['departTarget'] = data['dept_target']
            del data['dept_target']
        return data
    
    class Meta(Base.Meta):
        model = CompleteTraining
 
class EmailSchema(Base):
    id = fields.Int(data_key="id")
    subject = fields.Str(data_key="subject")
    body = fields.Str(data_key="body")
    sender = fields.Str(data_key="from")
    recipient = fields.Str(data_key="to")
    making_phishing = fields.Int(data_key='makingPhishing',dump_only=True)
    department_id= fields.Int(data_key='departmentId', dump_only=True)
    sent_date = fields.DateTime(
        data_key="sentDate",
        format='iso',
        load_format='iso',
        dump_format='%Y-%m-%d %H:%M:%S'
    )
    employee = fields.Nested(
        'EmployeeSchema',
        only=['id', 'name'],
        data_key='employee',
        dump_only=True
    )
    emails = fields.List(
        fields.Nested('EmailSchema', exclude=['employee']),
        data_key='emails',
        dump_only=True
    )

 

    class Meta(Base.Meta):
        model = Email

 
class EventLogSchema(Base):
    id = fields.Int(dump_only=True)
    action = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    training_id  = fields.Int(required=True)
    employee_id = fields.Str( )
    department_id = fields.Str( )
    email_id = fields.Str()
    role_id = fields.Str()
    data = fields.Str()

    @pre_load
    def process_ids(self, data, **kwargs):
        for field in ['department_id', 'employee_id', 'email_id', 'role_id']:
            if field in data and isinstance(data[field], list):
                data[field.lower()] = json.dumps(data[field])
        return data

    @post_dump
    def process_ids_dump(self, data, **kwargs):
        for field in ['department_id', 'employee_id', 'email_id', 'role_id']:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    data[field] = []
        return data
    
    class Meta(Base.Meta):
        model = EventLog

# Schema instances for direct usage
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)
email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)

event_log_schema = EventLogSchema()
event_logs_schema = EventLogSchema(many=True)
complete_training_schema = CompleteTrainingSchema()
complete_trainings_schema = CompleteTrainingSchema(many=True)
# Export all schemas
__all__ = [
    'department_schema', 'departments_schema',
    'role_schema', 'roles_schema',
    'employee_schema', 'employees_schema',
    'training_schema', 'trainings_schema',
    'email_schema', 'emails_schema',
    'complete_training_schema','complete_trainings_schema'
    'event_log_schema', 'event_logs_schema'
]
