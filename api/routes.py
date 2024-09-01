from flask import jsonify, request,Blueprint
from models.user import User
from models.email import Email
from models.training import Training
from models.models import AuthToken, Url
from models.dashboard import DashboardItem, Table,Chart
from extensions import ma, db, session_scope

from models.schemas import  (user_schema, users_schema, 
    training_schema, trainings_schema, 
    emails_schema, 
    dashboard_item_schema, dashboard_items_schema
)
import random

routes=Blueprint('routes',__name__)

@routes.route('/')
def home():
    return "Welcom Email Test"

@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@routes.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@routes.route('/user',methods=['POST'])
def add_user():
    username=request.json['username']
    email = request.json['email']
    password=request.json['password']

    new_user =User(username=username,email=email,password_hash=password)

    db.extensions.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@routes.route('/training', methods=['POST'])
def create_training():
    data = request.json
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    required_fields = ['trainingName', 'trainingStart', 'trainingEnd', 'resourceUser']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    try:
        new_training = Training(
            trainingName=data['trainingName'],
            trainingDesc=data.get('trainingDesc', ''),
            trainingStart=data['trainingStart'],
            trainingEnd=data['trainingEnd'],
            resourceUser=data['resourceUser'],
            maxPhishingMail=data.get('maxPhishingMail', random.randint(1, 10))  # Default to a random numr if not provided
        )
        
        db.session.add(new_training)
        db.session.commit()
        
        return training_schema.jsonify(new_training), 201
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the training"}), 500

@routes.route('/training/bulk',methods=['POST'])
def create_trainings_bulk():
    try: 
        data=request.json
        new_trainings=[]
        for training_data in data:
            new_training = Training(
                trainingName=training_data['trainingName'],
                trainingDesc=training_data['trainingDesc'],
                trainingStart=training_data['trainingStart'],
                trainingEnd=training_data['trainingEnd'],
                resourceUser=training_data['resourceUser'],
                maxPhishingamil=training_data['maxPhishingamil']
            )
            new_trainings.append(new_training)

        with session_scope() as session:
            session.bulk_save_objects(new_trainings)
        return jsonify({"message":f"{len(new_trainings)} training success!" }),201
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
    

@routes.route('/training',methods =['GET'])
def get_trainings():
      try:
          all_trainings =Training.query.all()
          result=  trainings_schema.dump(all_trainings)
          return jsonify(result),200
      except Exception as e :
            return jsonify({"message": "An error occurred while retrieving trainings"}), 500


@routes.route('/dasdhboard',methods =["GET"])
def get_dashboard():
     try:
          total_trainings= Training.query.count()

          def calculate_avg_phishing_mails():
              with session_scope() as session:
                  avg_phishing_mails=session.query(db.func.avg(Training.maxPhishingMail)).scalar() or 0
                  print(f"Average Phishing Emailss : {avg_phishing_mails}")
                  return avg_phishing_mails
          avg_phishing_mails = calculate_avg_phishing_mails()

          dashboard_items=[
              DashboardItem(title="Total Trainings", value=str(total_trainings), description="Total numr of training"),
              DashboardItem(title="Avg Phishing MAils", value=f"{avg_phishing_mails:.2f}", description="Average numr of phishing mails per training") 
          ]
          result= dashboard_item_schema.dump(dashboard_items)
          return jsonify(result),200
     
     except Exception as e :
        return jsonify({"message":"Error from DashBoard items"}),500

@routes.route('/emails', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    return emails_schema.jsonify(emails)