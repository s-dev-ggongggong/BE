from extensions import session_scope
from models.training import Training
import json
import logging
 

logger = logging.getLogger(__name__)

def clean_dept_target_data():
    with session_scope() as session:
        trainings = session.query(Training).all()
        for training in trainings:
            try:
                if isinstance(training.dept_target, str):
                    dept_target = json.loads(training.dept_target)
                    if isinstance(dept_target, list):
                        training.dept_target = json.dumps(dept_target)
                    else:
                        training.dept_target = '[]'
                elif training.dept_target is None:
                    training.dept_target = '[]'
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in dept_target for training {training.id}: {training.dept_target}")
                training.dept_target = '[]'
        session.commit()

# 이 함수를 실행
clean_dept_target_data()