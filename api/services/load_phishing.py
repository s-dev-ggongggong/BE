from utils.logger import setup_logger
from utils.db_error_handlers import handle_db_errors
from models.email import EmailLog
from utils.constants import DATETIME_FORMAT
from datetime import datetime
logger = setup_logger(__name__)

@handle_db_errors
def create_phishing_email_log(email_obj):
    # EmailLog 모델의 필드에 맞게 수정
    phishing_log = EmailLog(
        sender=email_obj.recipient,
        recipient=email_obj.sender,
        subject=email_obj.subject,
        body=email_obj.body,
        sent_date=datetime.utcnow(),
        training_aid=email_obj.training_aid,
        sender_user_id=email_obj.recipient_user_id,
        recipient_user_id=email_obj.sender_user_id
    )
    logger.info(f"Created phishing email log for training {email_obj.training_aid or 'Unknown'}")
    return phishing_log

# 사용 예시
@handle_db_errors
def use_phishing_log(email_obj):
    phishing_log = create_phishing_email_log(email_obj)
    # 여기서 phishing_log를 사용...
    return phishing_log