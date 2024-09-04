from models import *
from models.schemas import *
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from flask import jsonify


def validate_training_data(data, many=False):
    """Validates training data, either single or multiple records."""
    try:
        if many:
            return trainings_schema.load(data), None
        return training_schema.load(data), None
    except ValidationError as err:
        return None, {"message": "Validation error", "errors": err.messages}


def create_training_record(training_data):
    """Creates a single Training record and adds it to the session."""
    new_training = Training(**training_data)
    
    # Assuming EventLog creation as per the current logic
    initial_event_log = EventLog(
        training_id=new_training.id,
        employee_id=new_training.employee_id,
        department_id=1,  # Assuming a default department id, adjust as needed
        position="Initial Position",
        email="initial@example.com",
        name="Initial Name",
        action="target_setting"
    )
    return new_training, initial_event_log

def success_response(data=None, message=None, status=200):
    response = {"success": True}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    return jsonify(response), status


   