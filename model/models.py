from app import db,ma
from marshmallow import fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
 
    def __init__(self,username,email,password_hash):
        self.username= username
        self.email=email
        self.password_hash =password_hash
    
    def __repr__(self):
        return '<User %r>' % self.username
    

    
class DashboardItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    
    def __init__(self, title, value, description=None):
        self.title = title
        self.value = value
        self.description = description

    def __repr__(self):
        return f'<DashboardItem {self.title}>'
    
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    sent_date = db.Column(db.DateTime, nullable=False)
    
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String(120), nullable=False)
    fields = db.relationship('FormField', backref='form', lazy=True)

class FormField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    field_name = db.Column(db.String(120), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)  # 예: 'text', 'checkbox', 'radio'

    def __repr__(self):
        return f'<FormField {self.field_name} ({self.field_type})>'

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart_type = db.Column(db.String(50), nullable=False)  # 예: 'Line', 'Bar', 'Pie'
    data = db.Column(db.Text, nullable=False)  # JSON 형태로 차트 데이터 저장
    options = db.Column(db.Text, nullable=True)  # JSON 형태로 차트 옵션 저장

    def __repr__(self):
        return f'<Chart {self.chart_type}>'


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    columns = db.Column(db.Text, nullable=False)  # JSON 형태로 열 이름 저장
    rows = db.Column(db.Text, nullable=False)  # JSON 형태로 행 데이터 저장

    def __repr__(self):
        return f'<Table {self.name}>'

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    widget_type = db.Column(db.String(50), nullable=False)  # 예: 'Card', 'Banner', 'Chart'
    settings = db.Column(db.Text, nullable=True)  # JSON 형태로 위젯 설정 저장

    def __repr__(self):
        return f'<Widget {self.widget_type}>'

class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(256), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('auth_tokens', lazy=True))

    def __repr__(self):
        return f'<AuthToken {self.token}>'

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Url {self.url}>'

# Schema definitions

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class DashboardItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DashboardItem

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

class AuthTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthToken

class UrlSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Url
class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
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
auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)
emails_schema = EmailSchema(many=True)
