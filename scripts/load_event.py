import os, sys, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from init import create_app

from datetime import datetime
from models.event_log import EventLog
from models.training import Training
from models.employee import Employee
from models.department import Department
from sqlalchemy.exc import IntegrityError, OperationalError
from extensions import session_scope


# 인코딩 감지 함수
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']
# JSON 파일 로드 함수
def load_json(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

def update_training_status_from_agent(training_id, new_status):
    app = create_app()
    with app.app_context():
        training = Training.query.get(training_id)
        if training:
            if new_status in ['RUN', 'FIN']:
                training.status = new_status
                db.session.commit()
                print(f"Training ID {training_id} status updated to {new_status}")
            else:
                print(f"Invalid status: {new_status}. Status must be 'RUN' or 'FIN'.")
        else:
            print(f"Training ID {training_id} not found.")

# EventLog 데이터를 로드하여 데이터베이스에 저장하는 함수
def load_event_logs(file_path):
    app = create_app()
    
    with app.app_context():
        with session_scope() as session:
            # JSON 파일에서 이벤트 로그 데이터를 로드
            event_logs_data = load_json(file_path)

            # 각 이벤트 로그를 처리하여 데이터베이스에 삽입
            for event_data in event_logs_data:
                try:
                    # 관련된 training, employee, department 존재 여부 확인
                    training = session.query(Training).filter_by(id=event_data['training_id']).first()
                    employee = session.query(Employee).filter_by(id=event_data['employee_id']).first()
                    department = session.query(Department).filter_by(id=event_data['department_id']).first()

                    if not training:
                        print(f"Training ID {event_data['training_id']} not found. Skipping event.")
                        continue
                    if not employee:
                        print(f"Employee ID {event_data['employee_id']} not found. Skipping event.")
                        continue
                    if not department:
                        print(f"Department ID {event_data['department_id']} not found. Skipping event.")
                        continue

                    # 새로운 이벤트 로그 생성
                    event_log = EventLog(
                        training_id=event_data['training_id'],
                        employee_id=event_data['employee_id'],
                        department_id=event_data['department_id'],
                        action=event_data['action']
                    )

                    # 데이터베이스에 삽입
                    session.add(event_log)

                except IntegrityError as e:
                    print(f"IntegrityError: {e}")
                    session.rollback()
                except OperationalError as e:
                    print(f"OperationalError: {e}")
                    session.rollback()

            # 모든 이벤트 로그를 커밋하여 저장
            session.commit()
            print("Event logs loaded successfully!")

if __name__ == '__main__':
    # 이벤트 로그를 저장한 JSON 파일 경로
    file_path = 'static/event_logs.json'
    load_event_logs(file_path)