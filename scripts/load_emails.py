import json,os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from datetime import datetime
from run import create_app, db
from models.email import Email
from sqlalchemy.exc import OperationalError, IntegrityError
from extensions import session_scope
import chardet


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return json.load(file)
0
def load_emails():
    app = create_app()
    with app.app_context():
        with session_scope() as session:
            # Load email data from emails.json
            email_data = load_json('static/emails.json')

            for email in email_data:
                retries = 5
                while retries > 0:
                    try:
                        email_obj = Email(
                            subject=email['subject'],
                            body=email['body'],
                            sender=email['sender'],
                            recipient=email['recipient'],
                            sentDate=datetime.strptime(email['sentDate'], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        session.add(email_obj)
                        break
                    except OperationalError as e:
                        if "database is locked" in str(e):
                            retries -= 1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise
                    except IntegrityError:
                        print(f"IntegrityError: Failed to insert email: {email['subject']}")
                        session.rollback()

            try:
                session.commit()
                print("All emails committed successfully!")
            except OperationalError as e:
                if "database is locked" in str(e):
                    print("Database is locked, retrying...")
                    time.sleep(0.5)
                    session.rollback()
                    session.commit()
                else:
                    raise
            except Exception as e:
                print(f"Error committing emails: {str(e)}")
                session.rollback()

if __name__ == "__main__":
    load_emails()
    print("Emails loaded successfully!")
