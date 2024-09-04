from extensions import db, ma
from marshmallow import fields

class Agent(db.Model):
    __tablename__='agents'
    __table_args__={'extend_existing':True}
    
    id = db.Column(db.Integer, primary_key=True)
    # ... other fields ...
    trainings = db.relationship('Training', back_populates='agent', lazy=True)
    
    name = db.Column(db.String(120), nullable=False) 
    value = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    

    def __init__(self,name,  value, description=None):
        self.name = name
        self.value = value
        self.description = description

    def __repr__(self):
        return f'<Agent {self.id}>'

class AgentLog(db.Model):
    __tablename__ = 'agent_logs'
    __table_args__={'extend_existing':True}
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), nullable=False)
    logLevel = db.Column(db.String(50), nullable=False)
    process = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    def __init__(self, timestamp, logLevel, process, message):
        self.timestamp = timestamp
        self.logLevel = logLevel
        self.process = process
        self.message = message

    def __repr__(self):
        return f"<AgentLog {self.timestamp} - {self.process}>"