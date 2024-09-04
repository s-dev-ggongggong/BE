from extensions import ma
from marshmallow import fields
from models import Department, Employee, Role, Training, Agent,AgentLog, EventLog, Form, FormField, Email, AuthToken, Url, DashboardItem

class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        include_relationships = True

class DepartmentSchema(Base):
    class Meta(Base.Meta):
        model = Department

class RoleSchema(Base):
    class Meta(Base.Meta):
        model = Role

class TrainingSchema(Base):
    class Meta(Base.Meta):
        model = Training
    employee = fields.Nested('EmployeeSchema', exclude=('trainings',), dump_only=True)
    event_logs = fields.List(fields.Nested('EventLogSchema', exclude=('training',)), dump_only=True)
    agent_id = fields.Int(data_key='agentId',allow_none=True)

class EmployeeSchema(Base):
    class Meta(Base.Meta):
        model = Employee
        exclude = ('password_hash',)
    trainings = fields.List(fields.Nested(TrainingSchema, exclude=('employee',)), dump_only=True)
    event_logs = fields.List(fields.Nested('EventLogSchema', exclude=('employee',)), dump_only=True)

class AgentSchema(Base):
    class Meta(Base.Meta):
        model = Agent
class AgentLogSchema(Base):
    class Meta(Base.Meta):
        model = AgentLog

class EventLogSchema(Base):
    class Meta(Base.Meta):
        model = EventLog

class FormFieldSchema(Base):
    class Meta(Base.Meta):
        model = FormField

class FormSchema(Base):
    class Meta(Base.Meta):
        model = Form
    fields = fields.Nested(FormFieldSchema, many=True)

class EmailSchema(Base):
    class Meta(Base.Meta):
        model = Email

class AuthTokenSchema(Base):
    class Meta(Base.Meta):
        model = AuthToken

class UrlSchema(Base):
    class Meta(Base.Meta):
        model = Url


class UserWithTrainingsSchema(Base):
    trainings = fields.List(fields.Nested(TrainingSchema(exclude=('employee',))), dump_only=True)


class TrainingWithUserSchema(Base):
    user = fields.Nested(EmployeeSchema(exclude=('trainings',)), dump_only=True)

class DashboardItemSchema(Base):
    class Meta:
        model = DashboardItem
        

# Schema instances
users_with_trainings_schema = UserWithTrainingsSchema()
trainings_with_users_schema = TrainingWithUserSchema()
dashboard_item_schema = DashboardItemSchema()
dashboard_items_schema = DashboardItemSchema(many=True)
trainings_with_users_schema = TrainingWithUserSchema(many=True)
users_with_trainings_schema = UserWithTrainingsSchema(many=True)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)

agent_schema = AgentSchema()
agents_schema = AgentSchema(many=True)
agent_log_schema = AgentLogSchema()
agent_logs_schema = AgentLogSchema(many=True)

event_log_schema = EventLogSchema()
event_logs_schema = EventLogSchema(many=True)

form_schema = FormSchema()
forms_schema = FormSchema(many=True)

email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)

auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)

url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)

# Export all schemas
__all__ = [
    'department_schema', 'departments_schema',
    'role_schema', 'roles_schema',
    'employee_schema', 'employees_schema',
    'training_schema', 'trainings_schema',
    'agent_schema', 'agents_schema',
    'event_log_schema', 'event_logs_schema',
    'form_schema', 'forms_schema',
    'email_schema', 'emails_schema',
    'auth_token_schema', 'auth_tokens_schema',
    'url_schema', 'urls_schema','dashboard_items_schema',
    'users_with_trainings_schema', 'trainings_with_users_schema',
    'agent_log_schema','agent_logs_schema'
]