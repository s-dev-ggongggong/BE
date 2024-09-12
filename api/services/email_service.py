from extensions import db
 
from models.schemas import email_schema, emails_schema
from utils.http_status_handler import handle_response, bad_request, not_found, server_error
from utils.logger import setup_logger
from datetime import datetime
from sqlalchemy import and_
from models.email import Email
from models.employee import Employee
from models.training import Training
import random

# Set up logger
logger = setup_logger(__name__)

def get_emails():
    try:
        emails = Email.query.all()
        result = emails_schema.dump(emails)
        logger.info("Successfully fetched emails")
        return {"data": result, "message": "Emails fetched successfully.", "status_code": 200}
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}", exc_info=True)
        return {"error": f"Error fetching emails: {str(e)}", "status_code": 500}

def get_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        logger.info(f"Successfully fetched email with ID: {email_id}")
        return {"data": email_schema.dump(email), "message": "Email fetched successfully.", "status_code": 200}
    except Exception as e:
        logger.error(f"Error fetching email: {str(e)}", exc_info=True)
        return {"error": f"Error fetching email: {str(e)}", "status_code": 500}

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

        from api.services.training_service import check_and_set_action_for_email
        
        action = check_and_set_action_for_email(email)
        if action:
            email.action = action
            db.session.commit()

        return {"data": email_schema.dump(email), "message": "Email created successfully.", "status_code": 201}
    except Exception as e:
        return {"error": f"Error during email creation: {str(e)}", "status_code": 500}

def update_email(email_id, data):
    try:
        email = Email.query.get_or_404(email_id)
        email.subject = data.get('subject', email.subject)
        email.body = data.get('body', email.body)
        email.sender = data.get('from', email.sender)
        email.recipient = data.get('to', email.recipient)
        email.target_aid = data.get('target_aid', email.target_aid)
        email.is_phishing = data.get('is_phishing', email.is_phishing)

        db.session.commit()
        logger.info(f"Email with ID {email_id} updated successfully")
        return {"data": email_schema.dump(email), "message": "Email updated successfully.", "status_code": 200}
    except Exception as e:
        logger.error(f"Error updating email: {str(e)}", exc_info=True)
        return {"error": f"Error updating email: {str(e)}", "status_code": 500}

def delete_email(email_id):
    try:
        email = Email.query.get_or_404(email_id)
        db.session.delete(email)
        db.session.commit()
        logger.info(f"Email with ID {email_id} deleted successfully")
        return {"data": True, "message": "Email deleted successfully.", "status_code": 200}
    except Exception as e:
        logger.error(f"Error deleting email: {str(e)}", exc_info=True)
        return {"error": f"Error deleting email: {str(e)}", "status_code": 500}
    


def generate_phishing_logs(data):
    try:
        if not data or 'training_id' not in data:
            return {"error": "Request body is empty or training_id is missing.", "status_code": 400}
        
        training_id = data['training_id']
        training = Training.query.get_or_404(training_id)
        
        # 현재 시간이 training start date와 같거나 이후인 이메일들을 찾습니다
        target_emails = Email.query.filter(
            and_(
                Email.sent_date >= training.training_start,
                Email.is_phishing == False
            )
        ).all()
        
        # 대상 부서와 역할을 리스트로 변환
        dept_targets = training.dept_target.split(',')
        role_targets = training.role_target.split(',')
        
        # 대상 부서와 역할에 해당하는 직원들을 찾습니다
        target_employees = Employee.query.filter(
            and_(
                Employee.department_name.in_(dept_targets),
                Employee.role_name.in_(role_targets)
            )
        ).all()
        
        logs = []
        for email in target_emails:
            # 발신자와 수신자를 변경합니다
            original_sender = email.sender
            email.sender = f"phishing_{original_sender}"
            
            # 대상 직원 중 무작위로 수신자를 선택합니다
            if target_employees:
                random_employee = random.choice(target_employees)
                email.recipient = random_employee.email
            
            email.is_phishing = True
            email.training_id = training_id
            
            log = {
                "email_id": email.id,
                "original_sender": original_sender,
                "new_sender": email.sender,
                "new_recipient": email.recipient,
                "phishing_flag_set_at": datetime.utcnow().isoformat()
            }
            logs.append(log)
        
        db.session.commit()
        
        return {"data": logs, "message": "Phishing logs generated successfully.", "status_code": 200}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generating phishing logs: {str(e)}", exc_info=True)
        return {"error": f"Error generating phishing logs: {str(e)}", "status_code": 500}
    

def send_phishing_emails(training_id, employee_list):
    try:
        training = Training.query.get(training_id)
        if not training:
            return {"error": "Training not found", "status_code": 404}
        
        email_template = training.email_template if hasattr(training, 'email_template') else "Default Email Template"
        
        sent_emails = []
        for employee in employee_list:
            sent_emails.append({
                "employee_id": employee["id"],
                "email": employee["email"],
                "sent_at": datetime.utcnow().isoformat(),
                "email_body": email_template
            })
        return {"data": sent_emails, "message": "Phishing emails sent", "status_code": 200}
    except Exception as e:
        logger.error(f"Error sending phishing emails: {str(e)}", exc_info=True)
        return {"error": f"Error sending phishing emails: {str(e)}", "status_code": 500}

def check_and_set_action_for_email(email_id):
    try:
        email = Email.query.get(email_id)
        if not email:
            return {"error": "Email not found", "status_code": 404}
        
        training = Training.query.get(email.training_id) if hasattr(email, 'training_id') else None
        if training and training.training_start <= datetime.utcnow():
            action = "targetSetting"
            email.action = action
            db.session.commit()
            return {"message": f"Action '{action}' set for email", "status_code": 200}
        return {"message": "No action needed for the email", "status_code": 200}
    except Exception as e:
        logger.error(f"Error checking email action: {str(e)}", exc_info=True)
        return {"error": f"Error checking email action: {str(e)}", "status_code": 500}