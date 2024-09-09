import json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from sqlalchemy import inspect
from models.training import Training
from extensions import session_scope, db
from run import create_app
from datetime import datetime
from models.schemas import training_schema, trainings_schema
from marshmallow import ValidationError

app = create_app()

def update_training_status():
    with app.app_context():
        current_date = datetime.utcnow().date()
        
        trainings = Training.query.all()
        for training in trainings:
            if training.trainingEnd < current_date:
                training.status = 'FIN'
            elif training.trainingStart <= current_date <= training.trainingEnd:
                training.status = 'RUN '
            else:
                training.status = 'PLAN'

        db.session.commit()

def load_trainings(file_path):
    print("Starting load_trainings function...")
    
    update_training_status()
    print("Training statuses updated.")

    print("Loading training data from file...")
    with open(file_path, 'r') as file:
        trainings_data = json.load(file)
        print(f"Loaded {len(trainings_data)} training records from file.")
    
    # Validate data using schema
    try:
        validated_data = trainings_schema.load(trainings_data)
    except ValidationError as validation_errors:
        print(f"Data validation errors: {validation_errors}")
        return

    with app.app_context():
        try:
            with session_scope() as session:
                # Clear existing trainings
                Training.query.delete()

                # Add new trainings
                for item in validated_data:
                    #training = Training(**item)
                    session.add(item)
                
                session.commit()
                print(f'Successfully inserted {len(validated_data)} trainings into DB')
        except Exception as e:
            print(f"Error inserting data into DB: {str(e)}")
            return

    print("Attempting to send data to API...")
    # try:
    #     response = requests.post('http://localhost:8000/training/bulk', json=trainings_data, timeout=5)
    #     print(f"API Response Status Code: {response.status_code}")
    #     print("API Response:", response.json())
    #     response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     print(f"API request error: {str(e)}")

    print("load_trainings function completed.")

if __name__ == '__main__':
    print("Script started.")
    with app.app_context():
        inspector = inspect(db.engine)
        columns = inspector.get_columns('trainings')
        print("Columns in 'trainings' table:")
        for column in columns:
            print(column['name'])
    load_trainings('static/trainings.json')
    print("Script ended.")