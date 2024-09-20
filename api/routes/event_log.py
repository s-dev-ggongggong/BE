# api/routes/event_log.py
from flask import Blueprint, request, jsonify
from api.services import event_service
from utils.api_error_handlers import api_errorhandler, success_response
from marshmallow import ValidationError

event_log_bp = Blueprint('event_log_bp', __name__)

@api_errorhandler(event_log_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

@event_log_bp.route('/', methods=['GET'])
def get_all_event_logs():
    logs, status = event_service.get_all_event_logs()
    return success_response(data=logs, message="Event logs fetched 성공", status=status)

@event_log_bp.route('/<int:id>', methods=['GET'])
def get_event_log(id):
    log, status = event_service.get_event_log_by_id(id)
    return success_response(data=log, message=f"Event log {id} fetched 성공", status=status)
 

@event_log_bp.route('/<int:training_id>', methods=['PUT'])
def update_event_log(training_id):
    try:
        data = request.get_json()
        result, status = event_service.handle_event_log(training_id, data.get('data'))
        return success_response(data=result, message="Event log updated 성공", status=status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@event_log_bp.route('/<int:id>', methods=['DELETE'])
def delete_event_log(id):
    try:
        result, status = event_service.delete_event_log(id)
        return success_response(data=result, message="Event log deleted 성공", status=status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500