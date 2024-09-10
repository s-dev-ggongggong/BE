from flask import Blueprint, request, jsonify
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import handle_response, bad_request, not_found, server_error

training_bp = Blueprint('training_bp', __name__)

@api_errorhandler(training_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

# Route: Get all trainings
@training_bp.route('/', methods=['GET'])
def get_all_trainings():
    try:
        response, status = training_service.get_all_trainings()
        return handle_response(status, data=response, message="Trainings fetched successfully")
    except Exception as e:
        return server_error(f"Error fetching trainings: {str(e)}")

# Route: Get training by ID
@training_bp.route('/<int:id>', methods=['GET'])
def get_training(id):
    try:
        response, status = training_service.get_training_by_id(id)
        if status == 404:
            return not_found(f"Training with ID {id} not found")
        return handle_response(status, data=response, message=f"Training ID {id} fetched successfully")
    except Exception as e:
        return server_error(f"Error fetching training: {str(e)}")

# Route: Create new training
@training_bp.route('/', methods=['POST'])
def create_training():
    try:
        data = request.get_json()
        if not data:
            return bad_request("No data provided")
        response, status = training_service.create_new_training(data)
        return handle_response(status, data=response, message="Training created successfully")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error creating training: {str(e)}")

# Route: Update a training
@training_bp.route('/<int:id>', methods=['PUT'])
def update_training(id):
    try:
        data = request.get_json()
        if not data:
            return bad_request("No data provided")
        response, status = training_service.update_training(id, data)
        if status == 404:
            return not_found(f"Training with ID {id} not found")
        return handle_response(status, data=response, message=f"Training ID {id} updated successfully")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error updating training: {str(e)}")

# Route: Delete a training
@training_bp.route('/<int:id>', methods=['DELETE'])
def delete_training(id):
    try:
        response, status = training_service.delete_training(id)
        if status == 404:
            return not_found(f"Training with ID {id} not found")
        return handle_response(status, data=response, message=f"Training ID {id} deleted successfully")
    except Exception as e:
        return server_error(f"Error deleting training: {str(e)}")
