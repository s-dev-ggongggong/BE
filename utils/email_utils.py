from utils.email_utils import handle_email_errors
from models.email import PhishingEmailLog
from utils.logger import logging 
from models.phishing_email_log import PhishingEmailLog
logger = logging.getLogger(__name__)

@handle_email_errors

def create_phishing_email_log(email):
    return PhishingEmailLog(
        sender=email.sender,
        recipient=email.recipient,
        subject=email.subject,
        body=email.body,
        sent_date=email.sent_date,
        training_aid=email.training_aid
    )
# Example usage:
# @handle_email_errors
# def some_email_function(email_obj):
#     # Function logic here
#     pass