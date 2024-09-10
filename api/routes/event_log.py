from flask import Blueprint, request, jsonify
from api.services import event_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import handle_response, bad_request, not_found, server_error

event_log_bp = Blueprint('event_log_bp', __name__)

@api_errorhandler(event_log_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

# Route: Get all event logs
@event_log_bp.route('/', methods=['GET'])
def get_all_event_logs():
    try:
        response, status = event_service.get_all_event_logs()
        return handle_response(status, data=response, message="Event logs fetched successfully")
    except Exception as e:
        return server_error(f"Error fetching event logs: {str(e)}")

# Route: Get event log by ID
@event_log_bp.route('/<int:id>', methods=['GET'])
def get_event_log(id):
    try:
        response, status = event_service.get_event_log_by_id(id)
        if status == 404:
            return not_found(f"Event log with ID {id} not found")
        return handle_response(status, data=response, message=f"Event log ID {id} fetched successfully")
    except Exception as e:
        return server_error(f"Error fetching event log: {str(e)}")

# Route: Create new event log
@event_log_bp.route('/', methods=['POST'])
def create_event_log():
    try:
        data = request.get_json()
        if not data:
            return bad_request("No data provided")
        response, status = event_service.create_new_event_log(data)
        return handle_response(status, data=response, message="Event log created successfully")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error creating event log: {str(e)}")

# Route: Update an event log
@event_log_bp.route('/<int:id>', methods=['PUT'])
def update_event_log(id):
    try:
        data = request.get_json()
        if not data:
            return bad_request("No data provided")
        response, status = event_service.update_event_log(id, data)
        if status == 404:
            return not_found(f"Event log with ID {id} not found")
        return handle_response(status, data=response, message=f"Event log ID {id} updated successfully")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(f"Error updating event log: {str(e)}")

# Route: Delete an event log
@event_log_bp.route('/<int:id>', methods=['DELETE'])
def delete_event_log(id):
    try:
        response, status = event_service.delete_event_log(id)
        if status == 404:
            return not_found(f"Event log with ID {id} not found")
        return handle_response(status, data=response, message=f"Event log ID {id} deleted successfully")
    except Exception as e:
        return server_error(f"Error deleting event log: {str(e)}")
