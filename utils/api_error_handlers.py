from functools import wraps
from flask import jsonify
from marshmallow import ValidationError
from utils.logger import setup_logger

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
    from models.schemas import TrainingSchema
    from models.schemas import training_schema, trainings_schema  # Make sure to import the schemas here

    """Validates training data using Marshmallow schemas."""
    schema = TrainingSchema()
    try:
        # 데이터 변환 및 유효성 검사
        validated_data = schema.load(data)
        return validated_data
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        raise err
def success_response(data=None, message=None, status=200):
    """Generates a success response with optional data and message."""
    response = {"success": True}
    if message:
        logger.info(f"Success message: {message}")
        response["message"] = message
    if data:
        response["data"] = data
    return jsonify(response), status
