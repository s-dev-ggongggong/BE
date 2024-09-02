from extensions import db, ma
from marshmallow import fields, validate
from models.dashboard import DashboardItem, Chart, Table, Widget
from models.email import Email
from models.user import User
from models.training import Training
from models.models import Url, AuthToken, Form, FormField
from models.agent import Agent


# Form Schema
class FormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Form
    fields = fields.Nested('FormFieldSchema', many=True)

# Form Field Schema
class FormFieldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FormField

# Chart Schema
class ChartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chart

# Table Schema
class TableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Table

# Widget Schema
class WidgetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Widget

# Dashboard Item Schema
class DashboardItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DashboardItem


# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:    
        model = User
        include_fk = True
        load_instance = True

    trainings = fields.List(fields.Nested('TrainingSchema', exclude=('user',)), dump_only=True)

        

# Training Schema

class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        include_fk = True
        load_instance = True

    user = fields.Nested('UserSchema', exclude=('trainings',), dump_only=True)


    id = fields.Integer(dump_only=True)
    trainingName = fields.String(required=True)
    trainingDesc = fields.String(required=True)
    trainingStart = fields.Date(required=True)
    trainingEnd = fields.Date(required=True)
    resourceUser = fields.Integer(required=True)
    maxPhishingMail = fields.Integer(required=True)
    status = fields.String(required=True)
    department = fields.String(required=True)
    agentStartDate = fields.Date(allow_none=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    agentId = fields.Integer(allow_none=True)
    userId = fields.Integer(attribute='userId')
    





# Email Schema
class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email
        include_fk = True  # Include foreign key fields if they exist
        load_instance = True  # Deserialize to model instances

class EmailLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email
        include_fk = True  # Include foreign key fields if they exist
        load_instance = True 
# Auth Token Schema
class AuthTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthToken

# URL Schema
class UrlSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Url
class AgentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agent
        include_relationships = True
        load_instance = True

class UserWithTrainingsSchema(UserSchema):
    trainings = fields.List(fields.Nested(TrainingSchema(exclude=('user',))), dump_only=True)


class TrainingWithUserSchema(TrainingSchema):
    user = fields.Nested(UserSchema(exclude=('trainings',)), dump_only=True)

# Schema instances
trainings_with_users_schema = TrainingWithUserSchema(many=True)

users_with_trainings_schema = UserWithTrainingsSchema(many=True)
agent_schema = AgentSchema()
agents_schema = AgentSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)
emails_schema = EmailSchema(many=True)
training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)
trainings_with_users_schema = TrainingWithUserSchema(many=True)
dashboard_item_schema = DashboardItemSchema()
dashboard_items_schema = DashboardItemSchema(many=True)
form_schema = FormSchema()
forms_schema = FormSchema(many=True)
form_field_schema = FormFieldSchema()
form_fields_schema = FormFieldSchema(many=True)
chart_schema = ChartSchema()
charts_schema = ChartSchema(many=True)
table_schema = TableSchema()
tables_schema = TableSchema(many=True)
widget_schema = WidgetSchema()
widgets_schema = WidgetSchema(many=True)

# Export all schemas
__all__ = [
    'user_schema', 'users_schema', 'auth_token_schema', 'auth_tokens_schema',
    'url_schema', 'urls_schema', 'emails_schema', 'training_schema', 'trainings_schema',
    'dashboard_item_schema', 'dashboard_items_schema', 'form_schema', 'forms_schema',
    'form_field_schema', 'form_fields_schema', 'chart_schema', 'charts_schema',
    'table_schema', 'tables_schema', 'widget_schema', 'widgets_schema','agent_schema', 'agents_schema'  
]
