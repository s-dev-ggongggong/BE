from flask import Blueprint, request, jsonify
from models.training import Training
from models.user import User
from models.email import Email
from models.dashboard import DashboardItem
from models.agent import AgentLog
from extensions import db, ma, session_scope
from marshmallow import ValidationError
import random ,csv 
from datetime import datetime
import traceback
from models.schemas import users_with_trainings_schema ,trainings_with_users_schema

routes = Blueprint('training', __name__)

# Import all necessary schemas
from models.schemas import (
    user_schema, users_schema, 
    training_schema, trainings_schema, 
    emails_schema, 
    dashboard_item_schema, dashboard_items_schema
)

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

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@routes.route('/users/with-l', methods=['GET'])
def get_users_with_trainings():
    try:
        all_users = User.query.all()
        result = users_with_trainings_schema.dump(all_users)
        return jsonify(result)
    except Exception as e:
        print(f"Error retrieving users with trainings: {str(e)}")
        return jsonify({"error": str(e), "message": "An error occurred while retrieving users with trainings"}), 500
    
@routes.route('/training/create', methods=['POST'])
def create_training():
    data = request.json
    print("Retrieve",data)
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    required_fields = ['trainingName', 'trainingDesc', 'trainingStart', 'trainingEnd', 'resourceUser', 'maxPhishingMail', 'status', 'department']
 
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    try:
        training_data = training_schema.load(data)
        training_data.setdefault('maxPhishingMail', random.randint(1, 10))
        training_data.setdefault('status', 'pending')
        training_data.setdefault('department', '')

        new_training = Training(**training_data)

        db.session.add(new_training)
        db.session.commit()

    
        return training_schema.jsonify(new_training), 201
 
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400    
 
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the training"}), 500

@routes.route('/training/bulk', methods=['POST'])
def create_trainings_bulk():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging: print the received data
        validated_data = trainings_schema.load(data)

        # Bulk insert using SQLAlchemy
        db.session.bulk_save_objects(validated_data)
        db.session.commit()   
        return jsonify({"message": f"{len(validated_data)} trainings successfully added!"}), 201

    except ValidationError as ve:
        print(f"Validation error: {ve.messages}")
        return jsonify({"error": "Validation error", "details": ve.messages}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inserting data into DB: {e}")
        return jsonify({"error": str(e)}), 500

@routes.route('/training/read', methods=['GET'])
def get_trainings():
    try:
        all_trainings = Training.query.all()
        result = trainings_with_users_schema.dump(all_trainings)
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error retrieving trainings: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e), "message": "An error occurred while retrieving trainings"}), 500


@routes.route('/dashboard/read',methods =["GET"])
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

@routes.route('/agent/logs', methods=['POST'])
def receive_logs():
    try:
        logs = request.get_json()  # JSON 형식으로 로그 데이터를 받음
        print(f"Received logs: {logs}")

        with session_scope() as session:
            for log_entry in logs:
                agent_log = AgentLog(
                    subject=log_entry["subject"],
                    from_=log_entry["from"],
                    body=log_entry["body"]
                )
                session.add(agent_log)
            session.commit()

        return jsonify({"message": "Logs successfully stored"}), 201
    except Exception as e:
        print(f"Error processing logs: {str(e)}")
        return jsonify({"error": "Failed to store logs"}), 500

@routes.route('/agent/upload_csv',methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}),400
    
    file =request.files['file']

    if file.filename== '':
        return jsonify({"error": "no selected file "}),400
    
    if file and file.filename.endswith('.csv'):
        try:
            with session_scope() as session:
                csv_reader= csv.DictReader(file.stream)

                for row in csv_reader:
                    agent_log = AgentLog(
                        timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"),
                        logLevel=row['logLevel'],
                        process=row['process'],                       
                        message=row['message']
                    )
                    session.add(agent_log)
                session.commit()
            return jsonify({"message":"CSV file successfully processed and data stored"}),201
        except Exception as e :
            print(f"Error process CSV {str(e)}")
            return jsonify({"error":"Failed to process CSV file"}),500
    else:
        return jsonify({"error":"Invalid file format"}),400


@routes.route('/agent/logs', methods=['GET'])
def get_logs():
    try:
        with session_scope() as session:
            logs = session.query(AgentLog).all()
            logs_json = [{
                "timestamp": log.timestamp,
                "logLevel": log.logLevel,
                "process": log.process,
                "message": log.message
            } for log in logs]
            
        return jsonify(logs_json), 200
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        return jsonify({"error": "Failed to retrieve logs"}), 500


@routes.route('/emails/read', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    return emails_schema.jsonify(emails)