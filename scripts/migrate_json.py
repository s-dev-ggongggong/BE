from models.training import Training
from extensions import db
import json
import logging

logger = logging.getLogger(__name__)

def migrate_dept_target_data():
    trainings = Training.query.all()
    for training in trainings:
        if isinstance(training.dept_target, str):
            try:
                training.dept_target = json.loads(training.dept_target)
            except json.JSONDecodeError:
                training.dept_target = []
    db.session.commit()