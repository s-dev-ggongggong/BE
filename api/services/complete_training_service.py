# api/services/complete_training_service.py

from extensions import db
from models.complete_train import CompleteTraining
from models.schemas import complete_training_schema, complete_trainings_schema
from utils.http_status_handler import handle_response, server_error
import logging

logger = logging.getLogger(__name__)

def get_all_complete_trainings():
    try:
        complete_trainings = CompleteTraining.query.all()
        result = complete_trainings_schema.dump(complete_trainings)
        return result, 200
    except Exception as e:
        logger.error(f"Error fetching complete trainings: {str(e)}")
        return [], 500

def get_complete_training(id):
    try:
        complete_training = CompleteTraining.query.get(id)
        if not complete_training:
            return {"error": f"CompleteTraining with ID {id} not found"}, 404
        result = complete_training_schema.dump(complete_training)
        return result, 200
    except Exception as e:
        logger.error(f"Error fetching complete training: {str(e)}")
        return {"error": f"Error fetching complete training: {str(e)}"}, 500

def create_complete_training_service(data):
    try:
        complete_training = complete_training_schema.load(data, session=db.session)
        db.session.add(complete_training)
        db.session.commit()
        result = complete_training_schema.dump(complete_training)
        return result, 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating complete training: {str(e)}")
        return {"error": f"Error creating complete training: {str(e)}"}, 500
