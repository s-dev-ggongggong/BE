import json
import requests
from sqlalchemy import inspect
from models.training import Training
from extensions import session_scope ,db
from run import create_app
app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('trainings')
    print("Columns in 'trainings' table:")
    for column in columns:
        print(column['name'])



def validate_training_data(item):
    required_fields = ['trainingName', 'trainingDesc', 'trainingStart', 'trainingEnd', 'resourceUser', 'maxPhishingMail']
    for field in required_fields:
        if field not in item:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(item['maxPhishingMail'], int):
        raise ValueError(f"maxPhishingMail must be an integer, got {type(item['maxPhishingMail'])}")

def load_trainings(file_path):
    print("Starting load_trainings function...")
    
    with open(file_path, 'r') as file:
        trainings_data = json.load(file)
    print(f"Loaded {len(trainings_data)} training records from file.")
    
    # Validate data before inserting or sending to API
    for item in trainings_data:
        try:
            validate_training_data(item)
        except ValueError as e:
            print(f"Data validation error: {e}")
            return

    with app.app_context():
        try:
            with session_scope() as session:
                for item in trainings_data:
                    training = Training(
                        trainingName=item['trainingName'],
                        trainingDesc=item['trainingDesc'],
                        trainingStart=item['trainingStart'],
                        trainingEnd=item['trainingEnd'],   
                        resourceUser=item['resourceUser'],
                        maxPhishingMail=item['maxPhishingMail']  
                    )
                    session.add(training)
                    try:
                        training.resourceUser = int(training.resourceUser)
                    except ValueError:
                        print(f"Skipping invalid entry for {training.trainingName}")
                        continue
                Training.query.delete()
                session.commit()
                print(f'Successfully inserted {len(trainings_data)} trainings into DB')    
        except Exception as e:
            print(f"Error inserting data into DB: {str(e)}")
            return

    print("Attempting to send data to API...")
    print("Data being sent to API:")
    print(json.dumps(trainings_data, indent=2))
    try:
        response = requests.post('http://localhost:8000/training/bulk', json=trainings_data, timeout=5)
        print(f"API Response Status Code: {response.status_code}")
        print("API Response:", response.json())
        print("API Response:", response.text)  # Print the full response text
        response.raise_for_status()  # Raise an exception for bad stat
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server. Is it running on localhost:8000?")
    except requests.exceptions.Timeout:
        print("Error: API request timed out. The server might be slow or unresponsive.")
    except json.JSONDecodeError:
        print("Error: Received invalid JSON response from the API")
    except Exception as e:
        print(f"Unexpected error when calling API: {str(e)}")

    print("load_trainings function completed.")

if __name__ == '__main__':
    print("Script started.")
    load_trainings('static/trainings.json')
    print("Script ended.")