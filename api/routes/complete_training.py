from flask import Blueprint, request, jsonify
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
from api.services import complete_training_service
from utils.http_status_handler import  server_error
from api.services.training_service import update_training_service
from models.complete_train import CompleteTraining
from models.schemas import complete_training_schema, complete_trainings_schema
from datetime import datetime

complete_bp = Blueprint('complete_bp', __name__)

@api_errorhandler(complete_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@complete_bp.route('/', methods=['GET'])
def get_all_complete_trainings():
    try:
        response, status = complete_training_service.get_all_complete_trainings()
        return jsonify({"data": response, "message": "Complete trainings fetched successfully"}), status
    except Exception as e:
        return server_error(f"Error fetching complete trainings: {str(e)}")


@complete_bp.route('/<int:id>', methods=['GET'])
def get_complete_training(id):
    try:
        response, status = complete_training_service.get_complete_training(id)
        if status == 404:
            return jsonify({"error": f"CompleteTraining with ID {id} not found"}), 404
        return jsonify({"data": response, "message": f"CompleteTraining ID {id} fetched successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error fetching complete training: {str(e)}"}), 500


 
# Route: Update a training
@complete_bp.route('/', methods=['POST'])
def create_complete_training():
    try:
        data = request.get_json()
        response, status = complete_training_service.create_complete_training_service(data)
        if status != 201:
            return jsonify(response), status
        return jsonify({"data": response, "message": "Complete training created successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error creating complete training: {str(e)}"}), 500