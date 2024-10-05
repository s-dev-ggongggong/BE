from flask import json
from marshmallow import Schema, fields, EXCLUDE, post_load, ValidationError, pre_load, post_dump, validates
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
from marshmallow_enum import EnumField
from models.training import TrainingStatus 
from models.user_event_logs import UserEventLog

import logging
 

logger = logging.getLogger(__name__)

class DeptTargetField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        print(f"DeptTargetField _deserialize 호출: value={value}, attr={attr}")
        if value is None or value == []:
            return '[]'
        if isinstance(value, list):
            return json.dumps(value)  # 리스트를 JSON 문자열로 변환
        if isinstance(value, str):
            try:
                json.loads(value)  # JSON 형식 검증
                return value
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON string")
        raise ValidationError(f"Invalid type for dept_target: {type(value)}")

        
class JSONList(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format.")
        return []

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return json.dumps(value)
        raise ValidationError("Invalid input type. Expected a list.")



class FlexibleDateTime(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        # 우선 기본 형식으로 시도합니다.
        try:
            return super()._deserialize(value, attr, data, **kwargs)
        except ValidationError:
            pass

        # 추가적인 형식들을 시도합니다.
        date_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        for fmt in date_formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        raise ValidationError(f"지원되지 않는 날짜 형식입니다: {value}")
    
# Base Schema
class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE  

# Define schemas with data_key for camelCaseem
class DepartmentSchema(Base):
    id = fields.Int(data_key="id",dump_only=True)
    name = fields.Str(data_key="name")
    code1 = fields.Str(data_key="code1")
    code2 = fields.Str(data_key="code2")
    korean_name = fields.Str(data_key="koreanName")
    description = fields.Str(data_key="description")

 
    class Meta(Base.Meta):
        model = Department
        unknown = EXCLUDE  


class RoleSchema(Base):
    id = fields.Int(data_key="id", dump_only=True)
    name = fields.Str(data_key="name", required=True)
    korean_name = fields.Str(data_key="koreanName", required=True)

    class Meta(Base.Meta):
        model = Role

    @pre_load
    def process_role(self, data, **kwargs):
        role_name = data.get('roleName')
        if role_name:
            role = Role.query.filter_by(korean_name=role_name).first()
            if role:
                data['role_id'] = role.id
            else:
                raise ValidationError(f"Role '{role_name}' not found.")
            del data['roleName']
        return data

    @post_dump
    def add_roleName(self, data, **kwargs):
        if 'role' in data and data['role']:
            data['roleName'] = data['role']['korean_name']
            del data['role']
        return data


class EmployeeSchema(Base):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    role_name = fields.Str(data_key="roleName", required=False)
    department_id = fields.Int(data_key="departmentId")
    role_id = fields.Int(load_only=True, required=True)  # load_only으로 설정

    role = fields.Nested(RoleSchema, only=('id', 'name'))
    department = fields.Nested(DepartmentSchema, only=('id', 'name'))

    @post_load
    def make_employee(self, data, **kwargs):
        return data


    @pre_load
    def process_role(self, data, **kwargs):
        role_name = data.get('roleName')
        if not role_name:
            raise ValidationError({"roleName": ["Missing data for required field."]})
        
        role = Role.query.filter_by(korean_name=role_name).first()
        if role:
            data['role_id'] = role.id
        else:
            raise ValidationError({"roleName": [f"Role '{role_name}' not found."]})
        
        # 'roleName' 필드를 제거하여 Employee 생성자에 전달되지 않도록 함
        del data['roleName']
        return data


    @post_dump
    def add_roleName(self, data, **kwargs):
        if 'role' in data and data['role']:
            data['roleName'] = data['role']['korean_name']
            del data['role']
        return data
    
    class Meta:
        model = Employee
        include_fk = True
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE



from datetime import datetime

    
class TrainingSchema(SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    training_name = fields.Str(data_key="trainingName", required=True, allow_none=False)
    training_desc = fields.Str(data_key="trainingDesc", required=True, allow_none=False)
    training_start = fields.DateTime(data_key="trainingStart", format='iso', required=True, allow_none=False)
    training_end = fields.DateTime(data_key="trainingEnd", format='iso', required=True, allow_none=False)
    resource_user = fields.Int(data_key="resourceUser", required=True, allow_none=False)
    max_phishing_mail = fields.Int(data_key="maxPhishingMail", required=True, allow_none=False)
    dept_target = DeptTargetField(data_key="deptTarget", required=True, allow_none=True)

    status = EnumField(TrainingStatus, by_value=True, missing=TrainingStatus.PLAN)
    
    departments = fields.Nested('DepartmentSchema', many=True, only=['id', 'name'])

    created_at = fields.DateTime(dump_only=True, format='iso')
    is_finished = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True, format='iso')
    complete_training = fields.Nested('CompleteTrainingSchema', exclude=('original_training',))
    event_logs = fields.Nested('EventLogSchema', many=True, exclude=('training',))

    @validates('dept_target')
    def validate_dept_target(self, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value

    @post_load
    def make_training(self, data, **kwargs):
        print(f"@post_load data: {data}")
        # data가 dict 타입인지 확인하고 Training 객체가 아닌지 체크
        if isinstance(data, dict) and 'dept_target' in data:
            # dept_target 값이 JSON 문자열인지 확인하고 변환
            if isinstance(data['dept_target'], list):
                data['dept_target'] = json.dumps(data['dept_target'])
        return data  # Training 인스턴스를 생성하지 않고 딕셔너리 반환

    @post_dump
    def process_dept_target_dump(self, data, **kwargs):
        print(f"@post_dump data: {data}")
        # 데이터 덤프 시 data가 dict 타입인지 확인
        if isinstance(data, dict) and 'dept_target' in data and isinstance(data['dept_target'], str):
            try:
                # JSON 문자열을 리스트로 변환
                data['dept_target'] = json.loads(data['dept_target'])
            except json.JSONDecodeError:
                pass  # 잘못된 JSON 문자열일 경우 예외를 무시
        return data

    class Meta:
        model = Training
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE

class EventLogSchema(Base):
    id = fields.Int(data_key="id")
    action = fields.Str(data_key="action")
    timestamp = fields.DateTime(data_key="timestamp", format='iso', load_format='iso', dump_format='%Y-%m-%d %H:%M:%S')
    training_id = fields.Int(data_key="trainingId")
    department_id = JSONList(data_key="departmentId")
    data = fields.Dict(data_key="data")
    training = fields.Nested('TrainingSchema', exclude=('event_logs',))




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
        include_relationships = True
        load_instance = True
    
 

class UserEventLogSchema(Base):


    id = fields.Int(dump_only=True)
    employee_id = fields.Int(required=True)
    training_id = fields.Int(required=True)
    name = fields.Str(required=True)
    department_id = fields.Int(required=True)
    email_id = fields.Str(required=True)
    event_type = fields.Str()
    timestamp = fields.DateTime(dump_only=True)
    data = fields.Str()

    @post_load
    def make_user_event_log(self, data, **kwargs):
        return UserEventLog(**data)

    class Meta(Base.Meta):
        model = UserEventLog
        include_fk = True
        sqla_session = db.session


class CompleteTrainingSchema(Base):
    id = fields.Int(dump_only=True)
    original_id = fields.Int(required=True, load_only=True)
    completed_at = fields.DateTime(dump_only=True, format='iso')

    training_name = fields.Str(data_key="trainingName", required=True)
    training_desc = fields.Str(data_key="trainingDesc", required=True)
    training_start = FlexibleDateTime(data_key="trainingStart", required=True)
    training_end = FlexibleDateTime(data_key="trainingEnd", required=True)
    resource_user = fields.Int(data_key="resourceUser", required=True)
    max_phishing_mail = fields.Int(data_key="maxPhishingMail", required=True)
    dept_target = DeptTargetField(data_key="deptTarget", required=True, allow_none=True)
    departments = fields.Nested('DepartmentSchema', many=True, only=['id', 'name'])
    status = EnumField(TrainingStatus, by_value=True, missing=TrainingStatus.FIN)   

    original_training = fields.Nested('TrainingSchema', exclude=('complete_training',))
    
    
    @validates('dept_target')
    def validate_dept_target(self, key, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value
    
    @post_load
    def make_training(self, data, **kwargs):
        if 'dept_target' in data:
            data['dept_target'] = json.dumps(data['dept_target'])
        return Training(**data)
        
    @post_dump
    def process_dept_target_dump(self, data, **kwargs):
        if 'dept_target' in data and isinstance(data['dept_target'], list):
            data['dept_target'] = json.dumps(data['dept_target'])
        return data


    class Meta(Base.Meta):
        model = CompleteTraining
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE 


class EmailSchema(Base):
    id = fields.Int(data_key="id")
    subject = fields.Str(data_key="subject")
    body = fields.Str(data_key="body")
    sender = fields.Str(data_key="from")
    recipient = fields.Str(data_key="to")
    making_phishing = fields.Int(data_key='makingPhishing', dump_only=True)
    department_id = fields.Int(data_key="departmentId")
    sent_date = FlexibleDateTime(data_key="date", required=True)

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
        unknown = EXCLUDE


 

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
# 단일 객체와 객체 리스트를 위한 스키마 인스턴스 생성
user_event_log_schema = UserEventLogSchema()
user_event_logs_schema = UserEventLogSchema(many=True)

# Export all schemas
__all__ = [
    'department_schema', 'departments_schema',
    'role_schema', 'roles_schema',
    'employee_schema', 'employees_schema',
    'training_schema', 'trainings_schema',
    'email_schema', 'emails_schema',
    'complete_training_schema','complete_trainings_schema',
    'event_log_schema', 'event_logs_schema',
    'UserEventLogSchema', 'UserEventLogSchema'
]
