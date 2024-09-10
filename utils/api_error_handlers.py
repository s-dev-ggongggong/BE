from functools import wraps
from flask import jsonify
from marshmallow import ValidationError
from utils.logger import setup_logger
from models.schemas import training_schema, trainings_schema  # Make sure to import the schemas here

logger = setup_logger(__name__)

def api_errorhandler(blueprint):
    """Decorator to handle all API exceptions and log them."""
    def decorator(f):
        @blueprint.errorhandler(Exception)
        @wraps(f)
        def decorated_function(e):
            logger.error(f"API error: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
        return decorated_function
    return decorator

def validate_agent_ip(ip_addr):
    """Validates the agent IP address."""
    logger.info(f"Validating agent IP: {ip_addr}")
    # Add IP validation logic here if required
    pass

def validate_training_data(data, many=False):
    """Validates training data using Marshmallow schemas."""
    try:
        if many:
            logger.info("Validating multiple training data records.")
            return trainings_schema.load(data), None  # Ensure trainings_schema is properly imported
        logger.info("Validating single training data record.")
        return training_schema.load(data), None  # Ensure training_schema is properly imported
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        return None, {"message": "Validation error", "errors": err.messages}

def success_response(data=None, message=None, status=200):
    """Generates a success response with optional data and message."""
    response = {"success": True}
    if message:
        logger.info(f"Success message: {message}")
        response["message"] = message
    if data:
        response["data"] = data
    return jsonify(response), status
