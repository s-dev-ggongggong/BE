from extensions import db
 
from models.schemas import email_schema, emails_schema
from utils.http_status_handler import handle_response, bad_request, not_found, server_error
from utils.logger import setup_logger
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.init import Training ,Email
# Set up logger
logger = setup_logger(__name__)

def get_emails():
    try:
        emails = Email.query.all()
        logger.info("Successfully fetched emails")
        
        return handle_response(200, data=emails_schema.dump(emails), message="Emails fetched successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching emails: {str(e)}", exc_info=True)
        return server_error(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}", exc_info=True)
        return server_error(f"Error fetching emails: {str(e)}")

def get_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        logger.info(f"Successfully fetched email with ID: {email_id}")
        return handle_response(200, data=email_schema.dump(email), message="Email fetched successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching email: {str(e)}", exc_info=True)
        return server_error(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching email: {str(e)}", exc_info=True)
        return server_error(f"Error fetching email: {str(e)}")

 
def create_email(data):
    try:
        email = Email(
            subject=data['subject'],
            body=data['body'],
            sender=data['from'],
            recipient=data['to'],
        )
        db.session.add(email)
        db.session.commit()

        # Import the function here to avoid circular imports
        from api.services.training_service import check_and_set_action_for_email
        
        # Check if action needs to be set based on training
        action = check_and_set_action_for_email(email)
        if action:
            email.action = action
            db.session.commit()

        return handle_response(201, data=email_schema.dump(email), message="Email created successfully.")
    except Exception as e:
        return server_error(f"Error during email creation: {str(e)}")

def update_email(email_id, data):
    try:
        if not data:
            logger.warning(f"Attempted to update email {email_id} with empty request body")
            return bad_request("Request body is empty.")
        
        email = Email.query.get_or_404(email_id)
        email.subject = data.get('subject', email.subject)
        email.body = data.get('body', email.body)
        email.sender = data.get('from', email.sender)
        email.recipient = data.get('to', email.recipient)
        email.target_aid = data.get('target_aid', email.target_aid)
        email.is_phishing = data.get('is_phishing', email.is_phishing)

        db.session.commit()
        logger.info(f"Email with ID {email_id} updated successfully")
        return handle_response(200, data=email_schema.dump(email), message="Email updated successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error during email update: {str(e)}", exc_info=True)
        return server_error(f"Database error during email update: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating email: {str(e)}", exc_info=True)
        return server_error(f"Error updating email: {str(e)}")

def delete_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        db.session.delete(email)
        db.session.commit()
        logger.info(f"Email with ID {email_id} deleted successfully")
        return handle_response(200, data=True, message="Email deleted successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error during email deletion: {str(e)}", exc_info=True)
        return server_error(f"Database error during email deletion: {str(e)}")
    except Exception as e:
        logger.error(f"Error deleting email: {str(e)}", exc_info=True)
        return server_error(f"Error deleting email: {str(e)}")

def generate_phishing_logs(data):
    try:
        if not data or 'email_id' not in data:
            logger.warning("Request body is empty or email_id is missing for phishing log generation")
            return bad_request("Request body is empty or email_id is missing.")
        
        email = Email.query.get_or_404(data['email_id'])
        logs, status = email.generate_phishing_logs(data)
        logger.info(f"Phishing logs generated for email ID {email.id}")
        return handle_response(status, data=logs, message="Phishing logs generated successfully.")
    except ValueError as e:
        logger.error(f"ValueError in phishing log generation: {str(e)}", exc_info=True)
        return bad_request(str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error during phishing log generation: {str(e)}", exc_info=True)
        return server_error(f"Database error during phishing log generation: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating phishing logs: {str(e)}", exc_info=True)
        return server_error(f"Error generating phishing logs: {str(e)}")

def track_email_response(data):
    try:
        if not data or 'email_id' not in data or 'action' not in data:
            logger.warning("Missing required fields: email_id or action in tracking email response")
            return bad_request("Missing required fields: email_id or action_taken.")
        
        email = Email.query.get_or_404(data['email_id'])
        email.action = data['action']
        email.response_time = datetime.utcnow()

        db.session.commit()
        logger.info(f"Tracked response for email ID {email.id}")
        return handle_response(200, data=email_schema.dump(email), message="Email response tracked successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error tracking email response: {str(e)}", exc_info=True)
        return server_error(f"Database error tracking email response: {str(e)}")
    except Exception as e:
        logger.error(f"Error tracking email response: {str(e)}", exc_info=True)
        return server_error(f"Error tracking email response: {str(e)}")

def check_and_set_action_for_email(email):
    """Check if the email is associated with a training and update the action if needed."""
    training = Training.query.get(email.training_id)  # Assuming email has a training_id
    if training and training.training_start <= datetime.utcnow():
        return "targetSetting"
    return None


def handle_event_log(trainings,event_log):
    if trainings.status == 'TargetSetting':
        # 메일 발송 로직 처리
        send_phishing_emails(trainings)
    elif event_log.action == 'RUN':
        # 이메일 로그 생성
        pass
def send_phishing_emails(training_id, employee_list):
    # Assuming the training contains an email template or some other information
    training = Training.query.get(training_id)
    email_template = training.email_template if training else "Default Email Template"

    sent_emails = []
    for employee in employee_list:
        sent_emails.append({
            "employee_id": employee["id"],
            "email": employee["email"],
            "sent_at": datetime.utcnow().isoformat(),
            "email_body": email_template  # Utilize training data here
        })
    return sent_emails