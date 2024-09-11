from flask import Blueprint, request, jsonify
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import  server_error
from api.services.training_service import update_training_service
from models.training import Training
from models.schemas import training_schema
from datetime import datetime

training_bp = Blueprint('training_bp', __name__)

@api_errorhandler(training_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

# Route: Get all trainings
@training_bp.route('/', methods=['GET']) 
def get_all_trainings():
    try:
        response, status = training_service.get_all_trainings()
        return jsonify({"data":response,"message":"Trainings fetched successfully"}),status
    except Exception as e:
        return server_error(f"Error fetching trainings: {str(e)}")

# Route: Get training by ID
@training_bp.route('/<int:id>', methods=['GET'])
def get_training(id):
    try:
        response, status = training_service.get_training(id)
        if status == 404:
            return jsonify({"error": f"Training with ID {id} not found"}), 404
        return jsonify({"data": response, "message": f"Training ID {id} fetched successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error fetching training: {str(e)}"}), 500
# Route: Create new training

@training_bp.route('/', methods=['POST'])
def create_training():
    data = request.get_json()
    if not data:
        return jsonify({"error":"No data provided"}), 400
    response, status = training_service.create_training(data)
    if status != 201:
        return jsonify({"error": response.get("error", "Unknown error occurred")}), status
    return jsonify({"data": response, 'message': "Training created successfully"}), status

@training_bp.route('/all', methods=['POST'])
def bulk_upload_trainings():
    try:
        data = request.json
        response, status = training_service.bulk_training(data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": f"Bulk upload error: {str(e)}"}), 500


# Route: Update a training
@training_bp.route('/<int:id>', methods=['PUT'])
def update_training_route(id):
    try:
        # Get the JSON data from the request
        data = request.get_json()
        print(f"Received ID: {id}")  # Verify if ID is passed correctly
        print(f"Received Data: {data}")  # Check the incoming data payload
        # Call the update_training function with id and data
        response, status  = update_training_service(id, data)
        return jsonify({"message": f"Training ID {id} updated successfully", "data": response}), status

    except Exception as e:
        return jsonify({"error": f"Error updating training: {str(e)}"}), 500

# Route: Delete a training
@training_bp.route('/<int:id>', methods=['DELETE'])
def delete_training(id):
    response, status = training_service.delete_training(id)
    if status != 200:
        return jsonify(response), status
    return jsonify({"data": response, "message": f"Training ID {id} deleted successfully"}), status
 