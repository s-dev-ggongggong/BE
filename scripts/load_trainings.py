import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from app import create_app
from extensions import db
from models.training import Training
from scripts.utils import load_json, parse_datetime

def load_trainings(file_path):
    app = create_app()
    with app.app_context():
        data = load_json(file_path)
        for item in data:
            existing = Training.query.filter_by(training_name=item['trainingName']).first()
            if not existing:
                training_data = {
                    'training_name': item['trainingName'],
                    'training_desc': item['trainingDesc'],
                    'training_start': parse_datetime(item['trainingStart']),
                    'training_end': parse_datetime(item['trainingEnd']),
                    'resource_user': item['resourceUser'],
                    'max_phishing_mail': item['maxPhishingMail'],
                    'dept_target': ','.join(item['deptTarget']),
                    'role_target': ','.join(item['roleTarget'])
                }
                training = Training(**training_data)
                db.session.add(training)
        db.session.commit()

if __name__ == '__main__':
    load_trainings('data/trainings.json')