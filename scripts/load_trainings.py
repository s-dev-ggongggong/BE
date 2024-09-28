import sys
import os

from marshmallow import ValidationError
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from app import create_app
from extensions import db
from flask import json
from models.training import Training
from models.schemas import training_schema
from sqlalchemy.exc import SQLAlchemyError

from scripts.utils import load_json, parse_datetime
from datetime import datetime
from marshmallow import ValidationError



def load_trainings(training_data):
    for item in training_data:
        item.pop('id', None)
        try:
            # dept_target을 JSON 문자열로 변환
            if 'dept_target' in item and isinstance(item['dept_target'], list):
                item['dept_target'] = json.dumps(item['dept_target'])
            
            training = training_schema.load(item, session=db.session)
            db.session.add(training)
        except ValidationError as err:
            print(f"Validation error for training '{item.get('trainingName', 'Unknown')}': {err.messages}")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"Error adding training '{item.get('trainingName', 'Unknown')}': {e}")
            db.session.rollback()

    try:
        db.session.commit()
        print("Trainings loaded successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error committing trainings to the database: {e}")

if __name__ == '__main__':
    load_trainings('data/trainings.json')