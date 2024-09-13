from flask import json
from marshmallow import fields, validates, ValidationError,validates_schema, pre_load, post_dump
from extensions import ma, db
from models.department import Department
from models.role import Role
from models.employee import Employee
from models.training import Training
from models.email import Email

from models.event_log import EventLog
from models.delete_train import DeletedTraining
# Base Schema
class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session

# Define schemas with data_key for camelCaseem
class DepartmentSchema(Base):
    id = fields.Int(data_key="id",dump_only=True)
    name = fields.Str(data_key="name",dump_only=True),
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
        id = fields.Int(data_key="id")
        name = fields.Str(data_key="name")
        korean_name = fields.Str(data_key="koreanName")
        class Meta(Base.Meta):
            model = Role

class EmployeeSchema(Base):
    id = fields.Int(data_key="id", dump_only=True)
    name = fields.Str(data_key="name")
    email = fields.Str(data_key="email")
    department_name = fields.Str(data_key="departmentName")
    role_name = fields.Str(data_key="roleName")
    admin_id = fields.Str(data_key="adminId", dump_only=True)
    admin_pw = fields.Str(data_key="adminPw", dump_only=True)

    class Meta(Base.Meta):
        model = Employee
        exclude = ('password',)
class TrainingSchema(Base):
    id = fields.Int(dump_only=True)
    training_name = fields.Str(data_key="trainingName")
    training_desc = fields.Str(data_key="trainingDesc")
    training_start = fields.DateTime(data_key="trainingStart",format='%Y-%m-%d %H:%M:%S')
    training_end = fields.DateTime(data_key="trainingEnd",format='%Y-%m-%d %H:%M:%S')
    resource_user = fields.Int(data_key="resourceUser")
    max_phishing_mail = fields.Int(data_key="maxPhishingMail")
    
    # Use lists here since you're receiving arrays in the JSON
    dept_target = fields.List(fields.Str(), data_key="deptTarget")
    role_target = fields.List(fields.Str(), data_key="roleTarget")
 
    created_at = fields.DateTime(dump_only=True,format='%Y-%m-%d %H:%M:%S')
    is_finished = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)

class EventLogSchema(Base):
    id = fields.Int(data_key="id")
    action = fields.Str(data_key="action")
    timestamp = fields.DateTime(data_key="timestamp", format='%Y-%m-%d %H:%M:%S')
    training_id = fields.Int(data_key="trainingId")
    department_id = fields.Int(data_key="departmentId")
    employee_id = fields.Str(data_key="employeeId")
    email_id = fields.Str(data_key="emailId")
    role_id = fields.Int(data_key="roleId")
    data = fields.Dict(data_key="data")

    @pre_load
    def process_ids(self, data, **kwargs):
        if 'employeeId' in data:
            if isinstance(data['employeeId'], list):
                data['employee_id'] = json.dumps(data['employeeId'])
            else:
                data['employee_id'] = data['employeeId']
        if 'emailId' in data:
            if isinstance(data['emailId'], list):
                data['email_id'] = json.dumps(data['emailId'])
            else:
                data['email_id'] = data['emailId']
        return data

    @post_dump
    def process_ids_dump(self, data, **kwargs):
        if 'employee_id' in data:
            try:
                data['employeeId'] = json.loads(data['employee_id'])
            except json.JSONDecodeError:
                data['employeeId'] = data['employee_id']
        if 'email_id' in data:
            try:
                data['emailId'] = json.loads(data['email_id'])
            except json.JSONDecodeError:
                data['emailId'] = data['email_id']
        return data

    @validates_schema
    def validate_ids(self, data, **kwargs):
        from models.department import Department
        from models.employee import Employee
        from models.email import Email
        from models.role import Role

        if 'department_id' in data:
            department = Department.query.get(data['department_id'])
            if not department:
                raise ValidationError(f"Department with ID {data['department_id']} does not exist.")

        if 'employee_id' in data:
            employee_ids = json.loads(data['employee_id']) if isinstance(data['employee_id'], str) else data['employee_id']
            for emp_id in employee_ids:
                employee = Employee.query.get(int(emp_id))
                if not employee:
                    raise ValidationError(f"Employee with ID {emp_id} does not exist.")

        if 'email_id' in data:
            email_ids = json.loads(data['email_id']) if isinstance(data['email_id'], str) else data['email_id']
            for email_id in email_ids:
                email = Email.query.get(int(email_id))
                if not email:
                    raise ValidationError(f"Email with ID {email_id} does not exist.")

        if 'role_id' in data:
            role = Role.query.get(data['role_id'])
            if not role:
                raise ValidationError(f"Role with ID {data['role_id']} does not exist.")

    class Meta(Base.Meta):
        model = EventLog
    
 
    class Meta(Base.Meta):
        model = Training
        load_instance=True
        include_fk=True


from marshmallow import Schema, fields

class DeletedTrainingSchema(Schema):
    id = fields.Int(dump_only=True)
    original_id = fields.Int(required=True)
    training_name = fields.Str(data_key="trainingName", required=True)
    training_desc = fields.Str(data_key="trainingDesc", required=True)
    training_start = fields.DateTime(data_key="trainingStart", required=True, format='%Y-%m-%d %H:%M:%S')
    training_end = fields.DateTime(data_key="trainingEnd", required=True, format='%Y-%m-%d %H:%M:%S')
    resource_user = fields.Int(data_key="resourceUser", required=True)
    max_phishing_mail = fields.Int(data_key="maxPhishingMail", required=True)
    dept_target = fields.List(fields.Str(), data_key="deptTarget", required=True)
    role_target = fields.List(fields.Str(), data_key="roleTarget", required=True)

    created_at = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    is_finished = fields.Boolean(dump_only=True)
    status = fields.Str()
    deleted_at = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = DeletedTraining
 
class EmailSchema(Base):
    id = fields.Int(data_key="id")
    subject = fields.Str(data_key="subject")
    body = fields.Str(data_key="body")
    sender = fields.Str(data_key="sender")
    recipient = fields.Str(data_key="recipient")
    sent_date = fields.DateTime(data_key="sentDate",format='%Y-%m-%d %H:%M:%S')
    class Meta(Base.Meta):
        model = Email

 
class EventLogSchema(Base):
    id = fields.Int(data_key="id")
    action = fields.Str(data_key="action")
    timestamp = fields.DateTime(data_key="timestamp",format='%Y-%m-%d %H:%M:%S')
    message = db.Column(db.String(255))  # 'message' 필드 추가
    
    training_id = fields.Int(data_key="trainingId")
    employee_id = fields.Int(data_key="employeeId")
    department_id = fields.Int(data_key="departmentId")
    data = fields.Dict(data_key="data")

    @validates_schema
    def validate_role_department(self, data, **kwargs):
        # Validate that the role exists
        role = Role.query.filter_by(name=data.get('role_name')).first()
        if not role:
            raise ValidationError(f"Role {data.get('role_name')} does not exist.")
        
        # Validate that the department exists
        department = Department.query.filter_by(name=data.get('department_name')).first()
        if not department:
            raise ValidationError(f"Department {data.get('department_name')} does not exist.")

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
deleted_training_schema = DeletedTrainingSchema()
deleted_trainings_schema = DeletedTrainingSchema(many=True)
# Export all schemas
__all__ = [
    'department_schema', 'departments_schema',
    'role_schema', 'roles_schema',
    'employee_schema', 'employees_schema',
    'training_schema', 'trainings_schema',
    'email_schema', 'emails_schema',
 
    'event_log_schema', 'event_logs_schema'
]
