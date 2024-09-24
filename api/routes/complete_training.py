from flask import Blueprint, request, jsonify
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
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
def get_all_trainings():
    try:
        response, status = training_service.get_all_trainings()
        return jsonify({"data":response,"message":"Trainings fetched successfully"}),status
    except Exception as e:
        return server_error(f"Error fetching trainings: {str(e)}")

@complete_bp.route('/<int:id>', methods=['GET'])
def get_training(id):
    try:
        response, status = training_service.get_training(id)
        if status == 404:
            return jsonify({"error": f"Training with ID {id} not found"}), 404
        return jsonify({"data": response, "message": f"Training ID {id} fetched successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error fetching training: {str(e)}"}), 500


 
# Route: Update a training
@complete_bp.route('/<int:id>', methods=['PUT'])
def update_training_route(id):
    try:

        data = request.get_json()
        print(f"Received ID: {id}") 
        print(f"Received Data: {data}")  
        response, status  = update_training_service(id, data)
        return jsonify({"message": f"Training ID {id} updated successfully", "data": response}), status

    except Exception as e:
        return jsonify({"error": f"Error updating training: {str(e)}"}), 500

 