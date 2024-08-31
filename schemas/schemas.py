from extensions import db, ma
from marshmallow import fields
from models.dashboard import DashboardItem, Form, FormField, Chart, Table, Widget
from models.email import Email
from models.user import User
from models.training import Training
from models.models import Url,AuthToken

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields=("id","username","email","department")
        

class FormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Form
    fields = fields.Nested('FormFieldSchema', many=True)

class FormFieldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FormField

class ChartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chart

class TableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Table

class WidgetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Widget


class DashboardItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DashboardItem

class TrainingSchema(ma.Schema):
    class Meta:
         fields=("id","trainingName","trainingDesc","trainingStart","trainigEnd","resourceUser","maxPhishingamil")
    trainingstart =fields.Date(format="%Y-%m-%d")
    trainingEnd= fields.Date(format="%Y-%m-%d")
    
class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email


class AuthTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthToken

class UrlSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Url

# Schema instances
 

user_schema = UserSchema()
users_schema = UserSchema(many=True)
auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)
emails_schema = EmailSchema(many=True)

training_schema= TrainingSchema()
trainings_schema= TrainingSchema(many=True)
       
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

#export all schemas
__all__=[
        'user_schema', 'users_schema', 'auth_token_schema', 'auth_tokens_schema',
    'url_schema', 'urls_schema', 'email_schema', 'emails_schema',
    'training_schema', 'trainings_schema', 'dashboard_item_schema',
    'dashboard_items_schema', 'form_schema', 'forms_schema',
    'form_field_schema', 'form_fields_schema', 'chart_schema', 'charts_schema',
    'table_schema', 'tables_schema', 'widget_schema', 'widgets_schema'
]