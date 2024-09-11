from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity  # JWT 인증 추가
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import server_error
from api.services.training_service import update_training_service
from models.training import Training
from models.schemas import training_schema
from datetime import datetime

training_bp = Blueprint('training_bp', __name__)

@api_errorhandler(training_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

# Route: Get all trainings (JWT 인증 필요)
@training_bp.route('/', methods=['GET'])
@jwt_required()  # JWT 인증 추가
def get_all_trainings():
    try:
        response, status = training_service.get_all_trainings()
        return jsonify({"data": response, "message": "Trainings fetched successfully"}), status
    except Exception as e:
        return server_error(f"Error fetching trainings: {str(e)}")

# Route: Get training by ID (JWT 인증 필요)
@training_bp.route('/<int:id>', methods=['GET'])
@jwt_required()  # JWT 인증 추가
def get_training(id):
    try:
        response, status = training_service.get_training(id)
        if status == 404:
            return jsonify({"error": f"Training with ID {id} not found"}), 404
        return jsonify({"data": response, "message": f"Training ID {id} fetched successfully"}), status
    except Exception as e:
        return jsonify({"error": f"Error fetching training: {str(e)}"}), 500

# Route: Create new training (JWT 인증 필요)
@training_bp.route('/', methods=['POST'])
@jwt_required()  # JWT 인증 추가
def create_training():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response, status = training_service.create_training(data)
    if status != 201:
        return jsonify({"error": response.get("error", "Unknown error occurred")}), status
    return jsonify({"data": response, 'message': "Training created successfully"}), status

# Route: Bulk upload trainings (JWT 인증 필요)
@training_bp.route('/all', methods=['POST'])
@jwt_required()  # JWT 인증 추가
def bulk_upload_trainings():
    try:
        data = request.json
        response, status = training_service.bulk_training(data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": f"Bulk upload error: {str(e)}"}), 500

# Route: Update a training (JWT 인증 필요)
@training_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()  # JWT 인증 추가
def update_training_route(id):
    try:
        data = request.get_json()
        print(f"Received ID: {id}")  # Verify if ID is passed correctly
        print(f"Received Data: {data}")  # Check the incoming data payload
        response, status = update_training_service(id, data)
        return jsonify({"message": f"Training ID {id} updated successfully", "data": response}), status
    except Exception as e:
        return jsonify({"error": f"Error updating training: {str(e)}"}), 500

# Route: Delete a training (JWT 인증 필요)
@training_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # JWT 인증 추가
def delete_training(id):
    response, status = training_service.delete_training(id)
    if status != 200:
        return jsonify(response), status
    return jsonify({"data": response, "message": f"Training ID {id} deleted successfully"}), status
