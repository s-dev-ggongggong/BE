import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from app import create_app
from extensions import db
from models.email import Email
from scripts.utils import load_json, parse_datetime

def load_emails(file_path):
    app = create_app()
    with app.app_context():
        data = load_json(file_path)
        for item in data:
            existing = Email.query.filter_by(subject=item['subject'], sender=item['from']).first()
            if not existing:
                email_data = {
                    'subject': item['subject'],
                    'body': item['body'],
                    'sender': item['from'],
                    'recipient': item['to'],
                    'sent_date': parse_datetime(item['date'])
                }
                email = Email(**email_data)
                db.session.add(email)
        db.session.commit()

if __name__ == '__main__':
    load_emails('data/emails.json')