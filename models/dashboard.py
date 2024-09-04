from extensions import db, ma
from marshmallow import fields


class DashboardItem(db.Model):

    __tablename__='dashboard_items'
    __table_args__={'extend_existing':True}
    
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
class Chart(db.Model):
    __tablename__= 'chart'
    __table_args__={'extend_existing':True}

    id = db.Column(db.Integer, primary_key=True)
    chartType = db.Column(db.String(50), nullable=False)  # 예: 'Line', 'Bar', 'Pie'
    data = db.Column(db.Text, nullable=False)  # JSON 형태로 차트 데이터 저장
    options = db.Column(db.Text, nullable=True)  # JSON 형태로 차트 옵션 저장

    def __repr__(self):
        return f'<Chart {self.chart_type}>'


class Table(db.Model):
    __tablename__= 'tables'
    __table_args__={'extend_existing':True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    columns = db.Column(db.Text, nullable=False)  # JSON 형태로 열 이름 저장
    rows = db.Column(db.Text, nullable=False)  # JSON 형태로 행 데이터 저장

    def __repr__(self):
        return f'<Table {self.name}>'

class Widget(db.Model):
    __tablename__= 'widget'
    __table_args__={'extend_existing':True}

    id = db.Column(db.Integer, primary_key=True)
    widgetType = db.Column(db.String(50), nullable=False)  # 예: 'Card', 'Banner', 'Chart'
    settings = db.Column(db.Text, nullable=True)  # JSON 형태로 위젯 설정 저장

    def __repr__(self):
        return f'<Widget {self.widgetType}>'

