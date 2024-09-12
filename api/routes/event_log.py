from flask import Blueprint, request, jsonify
from api.services import event_service
from utils.api_error_handlers import api_errorhandler
from utils.http_status_handler import handle_response, bad_request, not_found, server_error
from models.event_log import EventLog
event_log_bp = Blueprint('event_log_bp', __name__)

@api_errorhandler(event_log_bp)
def handle_api_error(error):
    return jsonify({"error": str(error)}), 500

# Route: Get all event logs
@event_log_bp.route('/', methods=['GET'])
def get_all_event_logs():
    logs = EventLog.query.all()  # Fetch all event logs
    logs_dict = [log.to_dict() for log in logs]  # Ensure serialization
    return logs_dict, 200

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

# Route: Create new event logf
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
        
        # Call the service to update the log
        response, status = event_service.update_event_log(id, data)
        return handle_response(status, data=response, message="Event log updated successfully")
    except Exception as e:
        return server_error(f"Error updating event log: {str(e)}")

# Route: Delete an event log
@event_log_bp.route('/<int:id>', methods=['DELETE'])
def delete_event_log(id):
    try:
        # Call the service function to delete the event log
        response, status = event_service.delete_event_log(id)
        return jsonify(response), status  # Use jsonify to ensure the response is serialized
    except Exception as e:
        return server_error(f"Error deleting event log: {str(e)}")


@event_log_bp.route('/agent_event/', methods=['POST'])
def agent_create_event_log():
    try:
        data = request.get_json()

        # Required fields, except 'action', since it will be set by the server
        required_fields = ['timestamp', 'trainingId', 'message']
        
        # Check if all required fields are present and not empty
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return bad_request(f"Missing or empty required fields: {', '.join(missing_fields)}")
        
        # Set 'action' to 'targetSetting' if not provided
        if not data.get('action'):
            data['action'] = 'targetSetting'
        
        # Call the service function to create the new log
        response, status = event_service.create_new_event_log(data)
        return handle_response(status, data=response, message="Event log created by agent successfully")
    except Exception as e:
        return server_error(f"Error creating event log from agent: {str(e)}")
