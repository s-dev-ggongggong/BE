from marshmallow import fields ,pre_load, post_dump
from extensions import ma, db
from models.department import Department
from models.role import Role
from models.employee import Employee
from models.training import Training
from models.email import Email
from models.auth_token import AuthToken
from models.event_log import EventLog
 
# Base Schema
class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session

# Define schemas with data_key for camelCaseem
class DepartmentSchema(Base):
    id = fields.Int(data_key="id")
    name = fields.Str(data_key="name")
    code1 = fields.Str(data_key="code1")
    code2 = fields.Str(data_key="code2")
    korean_name = fields.Str(data_key="koreanName")
    description = fields.Str(data_key="description")

    class Meta(Base.Meta):
        model = Department

class RoleSchema(Base):
        id = fields.Int(data_key="id")
        name = fields.Str(data_key="name")
        korean_name = fields.Str(data_key="koreanName")
        class Meta(Base.Meta):
            model = Role

class EmployeeSchema(Base):
    id = fields.Int(data_key="id")
    name = fields.Str(data_key="name")
    email = fields.Str(data_key="email")
    department_name = fields.Int(data_key="departmentName")
    role_name = fields.Int(data_key="roleName")
   
    class Meta(Base.Meta):
        model = Employee
        exclude = ('password',)
 
class TrainingSchema(Base):
    id = fields.Int(dump_only=True)
    training_name = fields.Str(data_key="trainingName")
    training_desc = fields.Str(data_key="trainingDesc")
    training_start = fields.Date(data_key="trainingStart")
    training_end = fields.Date(data_key="trainingEnd")
    resource_user = fields.Str(data_key="resourceUser")
    max_phishing_mail = fields.Int(data_key="maxPhishingMail")
    dept_target = fields.List(fields.Str(), data_key="deptTarget")
    role_target = fields.List(fields.Str(), data_key="roleTarget")


    class Meta(Base.Meta):
        model = Training
    @pre_load
    def process_lists(self, data, **kwargs):
        if 'deptTarget' in data:
            data['dept_target'] = ','.join(data['deptTarget'])
        if 'roleTarget' in data:
            data['role_target'] = ','.join(data['roleTarget'])
        return data

    @post_dump
    def process_strings(self, data, **kwargs):
        if 'dept_target' in data:
            data['deptTarget'] = data['dept_target'].split(',')
        if 'role_target' in data:
            data['roleTarget'] = data['role_target'].split(',')
        return data
class EmailSchema(Base):
    id = fields.Int(data_key="id")
    subject = fields.Str(data_key="subject")
    body = fields.Str(data_key="body")
    sender = fields.Str(data_key="sender")
    recipient = fields.Str(data_key="recipient")
    sent_date = fields.DateTime(data_key="sentDate")
    class Meta(Base.Meta):
        model = Email

class AuthTokenSchema(Base):
    id = fields.Int(data_key="id")
    token = fields.Str(data_key="token")
    employee_id = fields.Int(data_key="employeeId")
    created_at = fields.DateTime(data_key="createdAt")
    expires_at = fields.DateTime(data_key="expiresAt")  # 추가

    class Meta(Base.Meta):
        model = AuthToken

class EventLogSchema(Base):
    id = fields.Int(data_key="id")
    action = fields.Str(data_key="action")
    timestamp = fields.DateTime(data_key="timestamp")
    
    training_id = fields.Int(data_key="trainingId")
    employee_id = fields.Int(data_key="employeeId")
    department_id = fields.Int(data_key="departmentId")

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
auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)
event_log_schema = EventLogSchema()
event_logs_schema = EventLogSchema(many=True)

# Export all schemas
__all__ = [
    'department_schema', 'departments_schema',
    'role_schema', 'roles_schema',
    'employee_schema', 'employees_schema',
    'training_schema', 'trainings_schema',
    'email_schema', 'emails_schema',
    'auth_token_schema', 'auth_tokens_schema',
    'event_log_schema', 'event_logs_schema'
]
