from extensions import db
from models.init import Training, EventLog, Employee
from models.schemas import training_schema, trainings_schema, event_logs_schema
from utils.api_error_handlers import validate_training_data
from utils.http_status_handler import handle_response, bad_request, server_error
from marshmallow import ValidationError
from datetime import datetime

# 트레이닝 생성 함수
def create_training(data):
    try:
        if not data:
            return bad_request("요청 본문이 비어있습니다.")
        validate_training_data(data)  # 트레이닝 데이터 검증
        new_training = Training(**data)
        db.session.add(new_training)
        db.session.commit()
        return handle_response(201, data=training_schema.dump(new_training), message="트레이닝이 성공적으로 생성되었습니다.")
    except ValidationError as e:
        return bad_request(f"데이터 유효성 검증 오류: {str(e)}")
    except Exception as e:
        return server_error(f"트레이닝 생성 중 오류 발생: {str(e)}")

# 모든 트레이닝 조회 함수
def get_all_trainings():
    try:
        trainings = Training.query.all()
        return handle_response(200, data=trainings_schema.dump(trainings), message="모든 트레이닝을 성공적으로 조회했습니다.")
    except Exception as e:
        return server_error(f"트레이닝 조회 중 오류 발생: {str(e)}")

# 특정 트레이닝 조회 함수
def get_training(id):
    try:
        training = Training.query.get_or_404(id)
        return handle_response(200, data=training_schema.dump(training), message="트레이닝을 성공적으로 조회했습니다.")
    except Exception as e:
        return server_error(f"트레이닝 조회 중 오류 발생: {str(e)}")

# 트레이닝 업데이트 함수
def update_training(id, data):
    try:
        if not data:
            return bad_request("요청 본문이 비어있습니다.")
        training = Training.query.get_or_404(id)
        validate_training_data(data)  # 데이터 검증
        for key, value in data.items():
            setattr(training, key, value)
        db.session.commit()
        return handle_response(200, data=training_schema.dump(training), message="트레이닝이 성공적으로 업데이트되었습니다.")
    except ValidationError as e:
        return bad_request(f"데이터 유효성 검증 오류: {str(e)}")
    except Exception as e:
        return server_error(f"트레이닝 업데이트 중 오류 발생: {str(e)}")

# 트레이닝 삭제 함수
def delete_training(id):
    try:
        training = Training.query.get_or_404(id)
        db.session.delete(training)
        db.session.commit()
        return handle_response(200, data=True, message="트레이닝이 성공적으로 삭제되었습니다.")
    except Exception as e:
        return server_error(f"트레이닝 삭제 중 오류 발생: {str(e)}")

# 트레이닝 관련 이벤트 로그 조회 함수
def view_training_event_logs(id):
    try:
        event_logs = EventLog.query.filter_by(training_id=id).all()
        return handle_response(200, data=event_logs_schema.dump(event_logs), message="트레이닝 이벤트 로그를 성공적으로 조회했습니다.")
    except Exception as e:
        return server_error(f"이벤트 로그 조회 중 오류 발생: {str(e)}")

# 부서 및 역할 기준으로 사용자 필터링
def filter_users_by_criteria(department_id, role_id):
    try:
        query = Employee.query
        if department_id:
            query = query.filter_by(department_id=department_id)
        if role_id:
            query = query.filter_by(role_id=role_id)
        employees = query.all()
        result = [{"id": emp.id, "name": emp.name} for emp in employees]
        return handle_response(200, data=result, message="사용자 필터링을 성공적으로 수행했습니다.")
    except Exception as e:
        return server_error(f"사용자 필터링 중 오류 발생: {str(e)}")

# 벌크 트레이닝 생성 함수
def bulk_training(data):
    try:
        if not data:
            return bad_request("요청 본문이 비어있습니다.")
        trainings = []
        for training_data in data:
            validate_training_data(training_data)  # 각 트레이닝 데이터 검증
            new_training = Training(**training_data)
            trainings.append(new_training)
        db.session.add_all(trainings)
        db.session.commit()
        return handle_response(201, data=trainings_schema.dump(trainings), message="벌크 트레이닝이 성공적으로 생성되었습니다.")
    except ValidationError as e:
        return bad_request(f"데이터 유효성 검증 오류: {str(e)}")
    except Exception as e:
        return server_error(f"벌크 트레이닝 생성 중 오류 발생: {str(e)}")

# email 연동 decopuling
# File: services/training_service.py
from datetime import datetime

def check_and_set_action_for_email(email):
    """Check if the email is associated with a training and update the action if needed."""
    training = Training.query.get(email.training_id)  # Assuming email has a training_id
    if training and training.training_start <= datetime.utcnow():
        return "targetSetting"
    return None


import random
from sqlalchemy.sql import func



# event trigger 발생시
def handle_event_log(trainings,event_log):
    if trainings.status == 'TargetSetting':
        # 메일 발송 로직 처리
        send_phishing_emails(trainings)
    elif event_log.action == 'RUN':
        # 이메일 로그 생성
        create_train_log(trainings.created_at)

def get_random_employees(training_id, resource_user_count):
    # 랜덤으로 지정된 수의 직원을 선택하는 쿼리
    training = Training.query.get(training_id)
    random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
    
    for employee in random_employees:
        print(f'Selected Employee: {employee.name}')
    
    return random_employees

def send_phishing_emails(training_id, employee_list):
    training = Training.query.get(training_id)
    email_template = training.email_log  # Training과 관련된 이메일 템플릿을 가져옴

    for employee in employee_list:
        print(f'Sending email to: {employee.email}')
        # 여기서 실제 이메일 발송 로직을 추가 가능
        # 예를 들어, 이메일 본문 생성 및 메일 서버와의 연결 작업
