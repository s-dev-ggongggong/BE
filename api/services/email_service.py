import sys
import os

from marshmallow import ValidationError

from api.services.employee_service import get_employees_by_filters
from models.department import Department
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from extensions import db ,session_scope
 
from models.schemas import email_schema, emails_schema
from utils.logger import setup_logger
from datetime import datetime
from sqlalchemy import and_
from models.email import Email
from models.employee import Employee
from models.training import Training
import random

# Set up logger
logger = setup_logger(__name__)

def get_emails(search=None, employee_id=None):
    try:
        query = Email.query

        if employee_id:
            query = query.filter(Email.employee_id == employee_id)

        if search:
            query = query.join(Employee).filter(Employee.name.ilike(f'%{search}%'))

        emails = query.all()
        result = emails_schema.dump(emails)
        return {"data": result, "message": "Emails fetched successfully.", "status_code": 200}
    except Exception as e:
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
        # Validate and deserialize data
        email_data = email_schema.load(data)
        session = db.session

        # Prepare department filters
        department_filters = []
        if 'department' in data:
            dept_data = data['department']
            if 'name' in dept_data and dept_data['name']:
                department_filters.append(Department.name == dept_data['name'])
            if 'code1' in dept_data and dept_data['code1']:
                department_filters.append(Department.code1 == dept_data['code1'])
            if 'code2' in dept_data and dept_data['code2']:
                department_filters.append(Department.code2 == dept_data['code2'])
            if 'korean_name' in dept_data and dept_data['korean_name']:
                department_filters.append(Department.korean_name == dept_data['korean_name'])

        role_name = data.get('roleName')

        # Ensure at least one filter is provided
        if not department_filters and not role_name:
            return {"error": "At least one department field or roleName must be provided."}, 400

        # Get employees using the employee service function
        employees = get_employees_by_filters(
            role_name=role_name,
            department_filters=department_filters
        )

        if not employees:
            return {"error": "No employees found matching the criteria."}, 404

        # Create emails for the filtered employees
        sent_emails = []
        for employee in employees:
            new_email = Email(
                subject=email_data['subject'],
                body=email_data['body'],
                sender=email_data['from'],
                recipient=employee.email,
                sent_date=email_data.get('sent_date', datetime.utcnow()),
                is_phishing=email_data.get('is_phishing', False),
                employee_id=employee.id,
                department_id=employee.department_id
            )
            session.add(new_email)
            sent_emails.append(new_email)

        session.commit()
        result = emails_schema.dump(sent_emails)
        return {"data": result, "message": "Emails sent successfully.", "status_code": 201}
    except ValidationError as err:
        return {"error": err.messages}, 400
    except Exception as e:
        session.rollback()
        return {"error": f"Error during email creation: {str(e)}"}, 500

          

def update_email(email_id, data):
    try:
        email = Email.query.get_or_404(email_id)
        email.subject = data.get('subject', email.subject)
        email.body = data.get('body', email.body)
        email.sender = data.get('from', email.sender)
        email.recipient = data.get('to', email.recipient)
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
                "phishing_flag_set_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
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
                "sent_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
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
            return None
        
        training = Training.query.filter(
            Training.training_start <= email.sent_date,
            Training.training_end >= email.sent_date
        ).first()

        if training:
            email.training_id = training.id
            email.action = "targetSetting"
            db.session.commit()
            return "targetSetting"
        return None
    except Exception as e:
        logger.error(f"Error checking email action: {str(e)}", exc_info=True)
        return None