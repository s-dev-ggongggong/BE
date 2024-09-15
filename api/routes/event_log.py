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

@event_log_bp.route('/training/<int:training_id>', methods=['POST'])
def create_or_update_event_log(training_id):
    try:
        data = request.get_json().get('data')
        result, status = event_service.handle_event_log(training_id, data)
        return success_response(data=result, message="Event log created/updated 성공", status=status)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

@event_log_bp.route('/<int:id>', methods=['DELETE'])
def delete_event_log(id):
    result, status = event_service.delete_event_log(id)
    return success_response(data=result, message="Event log deleted 성공", status=status)

@event_log_bp.route('/multiple', methods=['POST'])
def handle_multiple_event_logs():
    try:
        data = request.get_json()
        training_ids = data.get('training_ids', [])
        event_data = data.get('data')
        results = event_service.handle_multiple_events(training_ids, event_data)
        return success_response(data=results, message="Multiple event logs processed 성공", status=200)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

@event_log_bp.route('/multiple', methods=['DELETE'])
def delete_multiple_event_logs():
    event_ids = request.get_json().get('event_ids', [])
    results = event_service.delete_multiple_events(event_ids)
    return success_response(data=results, message="Multiple event logs 삭제 성공", status=200)