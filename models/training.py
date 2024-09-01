from extensions import db, ma
from marshmallow import fields
from datetime import datetime
import random

class Training(db.Model):
        __tablename__ ='trainings'
        __table_args__={'extend_existing':True}


        id = db.Column(db.Integer, primary_key=True)
        trainingName = db.Column(db.String(100), nullable=False)
        trainingDesc = db.Column(db.String(500), nullable=False)
        trainingStart = db.Column(db.DateTime, nullable=True)
        trainigEnd= db.Column(db.DateTime, nullable=False)    
        resourceUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        maxPhishingamil = db.Column(db.Integer, default=0)
        
        user= db.relationship('User',backref=db.backref('training',lazy=True))

        def __init__(self, trainingName, trainingDesc, trainingStart,trainigEnd,resourceUser,maxPhishingamil):
            self.trainingName = trainingName
            self.trainingDesc = trainingDesc
            self.trainingStart = datetime.strptime(trainingStart,"%Y-%m-%d").date()
            self.trainigEnd = datetime.strptime(trainigEnd,"%Y-%m-%d").date()
            self.resourceUser = resourceUser
            self.maxPhishingamil=maxPhishingamil

        def __repr__(self):
              return f'<Training {self.trainingName}'