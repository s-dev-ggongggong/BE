import logging
from flask import Blueprint, request, jsonify
from api.services import training_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import server_error
from api.services.training_service import create_training_service, update_training_service, soft_delete_training, delete_training, update_training_status
from models.training import Training
from models.schemas import training_schema
from datetime import datetime
from extensions import db, session_scope
from utils.logger import setup_logger

logger = setup_logger(__name__)

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
        training = Training.query.get(id)
        if not training:
            return {'error': f'Training with ID {id} not found'}, 404

        # Use schema to serialize training
        result = training_schema.dump(training)

        return {
            'data': result,
            'message': f'Training ID {id} fetched successfully'
        }, 200
    except Exception as e:
        return {
            'error': f"Error fetching training: {str(e)}"
        }, 500
 

@training_bp.route('/', methods=['POST'])
def create_training():
    try:
        # JSON 데이터를 수신 및 검증
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No valid JSON provided"}), 400

        # JSON 데이터 출력 (디버깅용)
        logging.info(f"Received data: {data}")

        # 서비스 함수 호출
        response, status = create_training_service(data)
        
        return response, status

    except Exception as e:
        # 예외 발생 시 500 응답과 에러 메시지 반환
        logging.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@training_bp.route('/all', methods=['POST'])
def bulk_upload_trainings():
    logger.info("Bulk upload training request received.")  # Log request start
    try:
        # Access the request JSON body
        data = request.get_json()
        if not isinstance(data, list):  # Ensure the incoming data is a list
            return jsonify({"error": "Request body must be a list of training records."}), 400

        # Call the service to handle bulk training creation
        response_data, status_code = training_service.bulk_training(data)  # Fix double jsonify handling

        logger.info(f"Bulk training operation completed with status {status_code}.")  # Log only status code (no response object)
        
        # Directly return `response_data` without wrapping it in `jsonify` again
        return response_data, status_code

    except Exception as e:
        logger.error(f"Bulk upload error: {str(e)}")
        return jsonify({"error": f"Bulk upload error: {str(e)}"}), 500
    
@training_bp.route('/status', methods=['POST'])
def update_all_training_statuses():
    try:
        with session_scope() as session:
            trainings = Training.query.filter(Training.is_deleted == False).all()
            for training in trainings:
                update_training_status(training, session)
            session.commit()
        return jsonify({"message": "All training statuses updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route: Update a training
@training_bp.route('/<int:id>', methods=['PUT'])
def update_training_route(id):
    try:
        data = request.get_json()
        print(f"Received ID: {id}")
        print(f"Received Data: {data}")

        return  update_training_service(id, data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"Error updating training: {str(e)}"}, 500

# Route: Delete a training
# restore 불가 
# db 에서 완전 삭제
@training_bp.route('/<int:id>', methods=['DELETE'])
def hard_delete_training_route(id):
    response, status = training_service.delete_training_serivce(id)
    if status != 200:
        return jsonify(response), status
    return jsonify({"data": response, "message": f"Training ID {id} deleted successfully"}), status

# training 레코드 삭제 # isdelete랑 deleted_at 용 
# restore 가능
@training_bp.route('/<int:id>/soft', methods=['POST'])
def soft_delete_training_route(id):
    response, status = soft_delete_training(id)
    if status != 200:
        return jsonify(response), status
    return jsonify({"message": f"Training ID {id} successfully soft deleted"}), status

 

#삭제 복구하기 
@training_bp.route('/<int:id>/restore', methods=['POST'])
def restore_training(id):
    training = Training.query.filter_by(id=id).first()
    if training and training.is_deleted:
        training.is_deleted = False
        training.deleted_at = None
        db.session.commit()
        return jsonify({"message": "Training restored successfully"}), 200
    return jsonify({"error": "Training not found or not deleted"}), 404


# 랜덤 직원 호출
@training_bp.route('/<int:id>/rand/<int:count>', methods=['GET'])
def get_random_employees_route(id, count):
    # id: training_id, count: resource_user_count
    random_employees = training_service.get_random_employees(id, count)
    
    if random_employees:
        return jsonify({"data": random_employees, "message": f"Random {count} employees selected"}), 200
    else:
        return jsonify({"error": "Training not found or no employees available"}), 404