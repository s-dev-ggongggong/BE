import os, sys, time, json
from datetime import datetime
from typing import List, Dict
from sqlalchemy.exc import OperationalError, IntegrityError
import chardet
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from init import create_app
from models.email import Email
from extensions import session_scope, db
from utils.db_error_handlers import handle_db_errors

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to detect file encoding
def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# Load JSON data with detected encoding
def load_json(file_path: str) -> List[Dict]:
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

# Function to load emails from JSON into the database
@handle_db_errors
def load_emails(file_path: str = 'static/emails.json') -> None:
    with session_scope() as session:
        # Load email data from the JSON file
        email_data = load_json(file_path)

        for email in email_data:
            try:
                # Convert date format and create an Email instance
                sent_date = datetime.fromisoformat(email['sentDate'].rstrip('Z'))
                
                email_obj = Email(
                    training_aid=email.get('targetAid'),
                    sender=email['sender'],
                    recipient=email['recipient'],
                    sent_date=sent_date,
                    subject=email['subject'],
                    body=email['body']
                )

                # Add the email to the session
                session.add(email_obj)
            
            except KeyError as e:
                logger.error(f"Missing key {str(e)} in email: {email}")
            except ValueError as e:
                logger.error(f"Invalid date format in email: {email['sentDate']} - {str(e)}")
        
        # Commit all email records to the database
        session.commit()
        logger.info(f"Loaded {len(email_data)} emails successfully.")

# Main entry point for the script
@handle_db_errors
def main():
    app = create_app()
    with app.app_context():
        load_emails()

if __name__ == "__main__":
    main()