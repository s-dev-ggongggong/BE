import json
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy import func, or_
from models.employee import Employee  
from models.schemas import TrainingSchema, training_schema
from models.init import Training, EventLog, CompleteTraining
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.training import TrainingStatus
from utils.http_status_handler import handle_response, server_error
from flask_jwt_extended import create_access_token
from utils.string_utils import convert_dict_keys_to_snake_case  # Assuming you have this function
import logging
from datetime import datetime
from extensions import db ,session_scope

import re

logger = logging.getLogger(__name__)


def convert_date_string_to_datetime(date_string):
    try:
        # Adjust the date format to match the input JSON format
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        logging.error(f"Date conversion error: {str(e)}")
        raise

def to_snake_case(camel_str):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', camel_str).lower()

def map_json_to_model(data):

    mapped_data = {}
    for key, value in data.items():
        snake_key = to_snake_case(key)
        if isinstance(value, list):
            mapped_data[snake_key] = json.dumps(value)
        else:
            mapped_data[snake_key] = value
    return mapped_data

def validate_data(data):
    for key, value in data.items():
        if value in [None, "", [], {}] or (isinstance(value, str) and value.isspace()):
            return False
    return True

def convert_dict_keys_to_snake_case(data):
    def to_snake_case(string):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        return pattern.sub('_', string).lower()
    
    if isinstance(data, dict):
        return {to_snake_case(key): convert_dict_keys_to_snake_case(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_dict_keys_to_snake_case(item) for item in data]
    else:
        return data
    

def validate_training_data(data):
    required_fields = ['training_name', 'training_desc', 'training_start', 'training_end', 'resource_user', 'max_phishing_mail', 'dept_target']
    for field in required_fields:
        if field not in data:
            return False, f"{field} is required"
        if data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            return False, f"{field} cannot be empty or whitespace"
    
    # Additional validations
    if data['training_start'] >= data['training_end']:
        return False, "training_start must be earlier than training_end"
    
    if not isinstance(data['resource_user'], int) or data['resource_user'] <= 0:
        return False, "resource_user must be a positive integer"
    
    if not isinstance(data['max_phishing_mail'], int) or data['max_phishing_mail'] <= 0:
        return False, "max_phishing_mail must be a positive integer"
    
    if not isinstance(data['dept_target'], list) or len(data['dept_target']) == 0:
        return False, "dept_target must be a non-empty list"

    return True, None   

def check_training_duplicate(session, training):
    existing = session.query(Training).filter(
        Training.training_name == training.training_name,
        Training.training_start == training.training_start,
        Training.training_end == training.training_end
    ).first()
    return existing is not None


def get_event_log_by_id(id):
    event_log = EventLog.query.get(id)
    if event_log:
        event_log.department_id = json.loads(event_log.department_id)
    return event_log

def create_delete_event_log(training_id):
    event_log = EventLog(
        action="delete",
        timestamp=datetime.utcnow(),
        training_id=training_id,
        data="Training deleted"
    )
    return event_log





def create_event_log_for_training(training, session):
    try:
        print(4,training.dept_target)        
        dept_targets = training.dept_target

        if not dept_targets:
            logger.warning(f"No department targets for training ID {training.id}")
            return
        
        event_log = EventLog(
            action="targetSetting",
            timestamp=training.training_start,
            training_id=training.id,
            department_id=dept_targets,  # 다시 JSON 문자열로 저장
            data="agent"
        )
        session.add(event_log)
    except Exception as e:
        logger.error(f"Error creating event log for training: {str(e)}")
        raise


def update_training_status(training, session):
    now = datetime.utcnow()
    print("6")
    if training.training_start <= now < training.training_end:
        training.status = TrainingStatus.RUN
    elif now >= training.training_end:
        training.status = TrainingStatus.FIN
        training.is_finished = True
        
        # Update EventLog when training is finished
        event_log = EventLog.query.filter_by(training_id=training.id).first()
        print(event_log)
        if event_log:
            event_log.action = "remove"
            event_log.timestamp = now
# 트레이닝 생성 함수
# api/services/training_service.py




def create_training_service(data):
    with session_scope() as session:
        try:
            schema = TrainingSchema()
            print(1,data)
            new_training = schema.load(data, session=session)
            print(2,new_training)
            if check_training_duplicate(session, new_training): 
                return handle_response(400, message="동일한 트레이닝이 이미 존재합니다.")
            
            session.add(new_training)
            print(3)
            session.flush()
            print("?")
            create_event_log_for_training(new_training, session)
            print("5")
            update_training_status(new_training, session)
            session.commit()
            print("7")
            #result = schema.dump(new_training)
            
            return handle_response(200, message="트레이닝 생성 성공")
        except ValidationError as ve:
            return handle_response(400, message=f"데이터 검증 오류: {ve.messages}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating training: {str(e)}")
            return handle_response(500, message=f"트레이닝 생성 중 오류 발생: {str(e)}")


def get_all_trainings():
    with session_scope() as session:
        try:
            trainings = Training.query.all()
            schema = TrainingSchema()
            result = []
            for training in trainings:
                try:
                    dumped_training = schema.dump(training)
                    result.append(dumped_training)
                except Exception as e:
                    logger.error(f"Error dumping training {training.id}: {str(e)}")
                    result.append({"id": training.id, "error": str(e)})
            
            return {"data": result, "message": "Trainings fetched successfully"}, 200
        except Exception as e:
            logger.error(f"Error fetching trainings: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}", "data": None}, 500

# 특정 트레이닝 조회 함수수
# api/services/training_service.py

def get_training(id):
    with session_scope() as session:
        try:
            training = Training.query.get(id)
            if not training or training.is_deleted:
                return {'error': f'Training with ID {id} not found'}, 404

            result = training_schema.dump(training)
            return result, 200
        except ValidationError as ve:
            session.rollback()
            logger.error(f"Validation error: {ve.messages}")
            return {"error": f"Validation error: {ve.messages}"}, 400
        except Exception as e:
            session.rollback()
            logger.error(f"Exception occurred: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
        except IntegrityError as e:
            session.rollback()
            logger.error(f"IntegrityError: {str(e)}")
            return handle_response(400, message="Database integrity error.")


# 트레이닝 업데이트 함수


def update_training_service(id, data):
    with session_scope() as session:
        try:
            training = session.query(Training).get(id)
            if not training or training.is_deleted:
                return {"error": "Training not found"}, 404

            schema = TrainingSchema()
            training_data = schema.load(data, session=session, partial=True)

            for key, value in training_data.items():
                setattr(training, key, value)

            update_training_status(training, session)
            session.commit()

            result = schema.dump(training)
            return result, 200
        except ValidationError as ve:
            session.rollback()
            logger.error(f"Validation error: {ve.messages}")
            return {"error": f"Validation error: {ve.messages}"}, 400
        except Exception as e:
            session.rollback()
            logger.error(f"Exception occurred: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
        except IntegrityError as e:
            session.rollback()
            logger.error(f"IntegrityError: {str(e)}")
            return handle_response(400, message="Database integrity error.")
 

def handle_res(status_code, data=None, message=None):
    response = {
        "status": status_code,
        "message": message or "No message provided",  # Default message
        "data": data if data is not None else {}  # Ensure JSON serializable structure
    }
    
    return jsonify(response), status_code  # Properly return a JSON response


#### Updated `bulk_training` Function
# api/services/training_service.py


def bulk_training(data):
    if not data:
        return handle_response(400, message="요청 본문이 비어있습니다.")

    successful_trainings = []
    failed_trainings = []
    for training_data in data:
        result = create_training_service(training_data)
        if result[1] == 201:  # 성공적으로 생성된 경우
            successful_trainings.append(result[0]['data'])
        else:
            failed_trainings.append({
                "data": training_data,
                "error": result[0]['message']
            })

    return handle_response(200, data={
        "successful_trainings": successful_trainings,
        "failed_trainings": failed_trainings
    })

# 완전삭제
def delete_training_service(id):
    try:
        with session_scope() as session:
            training = session.query(Training).get(id)
            if not training:
                return {"error": "Training not found"}, 404
            
            # 관련된 EventLog 삭제
            EventLog.query.filter_by(training_id=id).delete()
            
            session.delete(training)
            session.commit()
            
            return {"message": "트레이닝이 성공적으로 삭제되었습니다."}, 200
    except Exception as e:
        session.rollback()
        return {"error": f"트레이닝 삭제 중 오류 발생: {str(e)}"}, 500
    except ValidationError as err:
        db.session.rollback()
        return {"error": err.messages}, 400
   

# 트레이닝 관련 이벤트 로그 조회 함수
def view_training_event_logs(id):
    try:
        event_logs = EventLog.query.filter_by(training_id=id).all()
        return  [t.to_dict() for t in event_logs],200
    except Exception as e:
        return {"error":f"이벤트 로그 조회 중 오류 발생: {str(e)}"}

# : Training 인스턴스를 기반으로 CompleteTraining 인스턴스를 생성하고, 필요한 관계를 복사하며, 세션에 추가하는 역할
def create_complete_training(training, session):
    complete_training = CompleteTraining(
        original_id=training.id,
        training_name=training.training_name,
        training_desc=training.training_desc,
        training_start=training.training_start,
        training_end=training.training_end,
        resource_user=training.resource_user,
        max_phishing_mail=training.max_phishing_mail,
        dept_target=training.dept_target,
        status=TrainingStatus.FIN if training.is_finished else training.status,
        completed_at=datetime.utcnow()
    )
    # 관계 복사
    complete_training.departments = training.departments.copy()
    session.add(complete_training)

# 완전삭제시 complete training 옮기기
def move_training_to_complete(training_id):
    with session_scope() as session:
        try:
            training = session.query(Training).get(training_id)
            if not training:
                return {"error": f"Training with ID {training_id} not found"}, 404

            # Training이 이미 완료되었거나 삭제되었는지 확인
            if not (training.is_finished or training.is_deleted):
                return {"error": f"Training with ID {training_id} is neither finished nor deleted"}, 400

            # CompleteTraining 생성 및 세션에 추가
            create_complete_training(training, session)

            session.commit()
            return {"message": f"Training with ID {training_id} moved to CompleteTraining"}, 200

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error occurred: {str(e)}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error occurred: {str(e)}")
            return {"error": "Unexpected error occurred"}, 500

#Training을 소프트 삭제하고, create_complete_training 함수를 호출하여 CompleteTraining을 생성
def soft_delete_training(id):
    with session_scope() as session:
        try:
            training = session.query(Training).get(id)
            if not training:
                return {"error": "Training not found"}, 404

            training.is_deleted = True
            training.deleted_at = datetime.utcnow()

            # CompleteTraining 생성
            create_complete_training(training, session)

            delete_log = create_delete_event_log(training.id)
            session.add(delete_log)

            session.commit()
            return {"message": "Training soft deleted successfully"}, 200

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error occurred: {str(e)}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error occurred: {str(e)}")
            return {"error": "Unexpected error occurred"}, 500


 
# Example function for getting random employees.
def get_random_employees(training_id, resource_user_count):
    training = Training.query.get(training_id)
    if training:
        random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
        return [{"id": emp.id, "name": emp.name, "email": emp.email} for emp in random_employees]
    return []
