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

logger = logging.getLogger(__name__)

def convert_date_string_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def to_snake_case(camel_str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel_str]).lstrip('_')

def map_json_to_model(data):
    mapped_data = {}
    for key, value in data.items():
        snake_key = to_snake_case(key)
        if isinstance(value, list):
            mapped_data[snake_key] = json.dumps(value)
        else:
            mapped_data[snake_key] = value
    return mapped_data

def validate_training_data(data,valid_depts, valid_roles):
 
    invalid_depts = set(data.get('deptTarget', [])) - valid_depts
    invalid_roles = set(data.get('roleTarget', [])) - valid_roles
 
    if invalid_depts or invalid_roles:
        return False, f"Invalid departments: {invalid_depts}, Invalid roles: {invalid_roles}",400
    return True, None


def convert_date_string_to_datetime(date_string):
    try:
        # Adjust the date format to match the input JSON format
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        logging.error(f"Date conversion error: {str(e)}")
        raise

def create_event_log_for_training(training, session):
    try:
        dept_targets = training.dept_target
        if not dept_targets:
            logger.warning(f"No department targets for training ID {training.id}")
            return
        
        event_log = EventLog(
            action="targetSetting",
            timestamp=training.training_start,
            training_id=training.id,
            department_id=json.dumps(dept_targets),
            data="agent"
        )
        session.add(event_log)
    except Exception as e:
        logger.error(f"Error creating event log for training: {str(e)}")
        raise

def update_training_status(training, session):
    now = datetime.utcnow()
    if training.training_start <= now < training.training_end:
        training.status = TrainingStatus.RUN
    elif now >= training.training_end:
        training.status = TrainingStatus.FIN
        training.is_finished = True
        
        # Update EventLog when training is finished
        event_log = EventLog.query.filter_by(training_id=training.id).first()
        if event_log:
            event_log.action = "remove"
            event_log.timestamp = now

def delete_training(training, session):
    training.is_deleted = True
    training.deleted_at = datetime.utcnow()
    
    # You might want to update or delete the associated EventLog
    event_log = EventLog.query.filter_by(training_id=training.id).first()
    if event_log:
        session.delete(event_log)
        
# 트레이닝 생성 함수
def create_training_service(data):
    with session_scope() as session:
        try:
            # Convert and validate incoming data
            mapped_data = {
                'training_name': data.get('trainingName', '').strip(),
                'training_desc': data.get('trainingDesc', '').strip(),
                'training_start': convert_date_string_to_datetime(data.get('trainingStart')),
                'training_end': convert_date_string_to_datetime(data.get('trainingEnd')),
                'dept_target':  data.get('deptTarget', '[]'), 
                'resource_user': data.get('resourceUser'),
                'max_phishing_mail': data.get('maxPhishingMail')
            }

            # Validate that mandatory fields are provided and not empty
            for field in ['training_name', 'training_desc', 'training_start', 'training_end', 'resource_user', 'dept_target']:
                if not mapped_data[field]:
                    return handle_response(400, message=f"{field.replace('_', ' ').capitalize()} is required and cannot be empty.")

            if not mapped_data['dept_target'] :
                return handle_response(400, message="Department target and role target must have at least one non-empty value each.")

            # Check for existing records with the same values
            existing_training = Training.query.filter(
                Training.training_name == mapped_data['training_name'],
                Training.training_desc == mapped_data['training_desc'],
                Training.training_start == mapped_data['training_start'],
                Training.training_end == mapped_data['training_end'],
                Training.max_phishing_mail == mapped_data['max_phishing_mail'],
                Training.resource_user == mapped_data['resource_user'],
                Training.dept_target == mapped_data['dept_target'],
            ).first()

            if existing_training:
                return handle_response(409, message="A training record with these details already exists.")

            # Create the new training object and save to the database
            new_training = Training(**mapped_data)
            session.add(new_training)
            session.flush()

            create_event_log_for_training(new_training, session)
            update_training_status(new_training, session)
            
            session.commit()
  
            # Serialize the created training and return success response
            response_data = training_schema.dump(new_training)
            return handle_response(201, data=response_data, message="Training created successfully.")

        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            db.session.rollback()
            return handle_response(400, message="Database integrity error.")

        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError: {str(e)}")
            db.session.rollback()
            return server_error(f"An error occurred while handling the request: {str(e)}")

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            db.session.rollback()
            return server_error(f"An unexpected error occurred: {str(e)}")
 
# 모든 트레이닝 조회 함수
def get_all_trainings():
    try:
        trainings = Training.query.all()
        result = []
        for training in trainings:
            try:
                result.append(training_schema.dump(training))
            except Exception as e:
                logging.error(f"Error processing training {training.id}: {str(e)}")
                # Optionally, you could include a placeholder or partial data for this training
        
        return {
            'data': result,
            'message': "Trainings fetched successfully"
        }, 200
    except Exception as e:
        logging.exception("Unexpected error in get_all_trainings")
        return {
            'data': {
                'error': f"트레이닝 조회 중 오류 발생: {str(e)}"
            },
            'message': "Trainings fetch failed"
        }, 500
    
# 특정 트레이닝 조회 함수
def get_training(id):
    try:
        training = Training.query.get(id)
        if not training:
            return {'error': f'Training with ID {id} not found'}, 404

        # Use schema to serialize training
        result = training_schema.dump(training)

        return {
            'data': result,
            'message': f'Training ID {id} fetched successfully'
        }, 200
    except Exception as e:
        return {
            'error': f"Error fetching training: {str(e)}"
        }, 500
    

# 트레이닝 업데이트 함수

def update_training_service(id, data):
    try:
        with session_scope() as session:

            # Find the training record
            training = Training.query.get(id)
            if not training:
                return handle_response(404, message="Training not found")

            # Prepare updated data
            updated_data = {}
            if 'trainingName' in data and data['trainingName'].strip():
                updated_data['training_name'] = data['trainingName'].strip()
            if 'trainingDesc' in data and data['trainingDesc'].strip():
                updated_data['training_desc'] = data['trainingDesc'].strip()
            if 'trainingStart' in data and data['trainingStart'].strip():
                updated_data['training_start'] = convert_date_string_to_datetime(data['trainingStart'].strip())
            if 'trainingEnd' in data and data['trainingEnd'].strip():
                updated_data['training_end'] = convert_date_string_to_datetime(data['trainingEnd'].strip())
            if 'deptTarget' in data:
                updated_data['dept_target'] = [item.strip() for item in data['deptTarget'] if item.strip()]
            if 'resourceUser' in data:
                # Handle resourceUser as either string or integer
                if isinstance(data['resourceUser'], str) and data['resourceUser'].strip():
                    updated_data['resource_user'] = data['resourceUser'].strip()
                elif isinstance(data['resourceUser'], int):
                    updated_data['resource_user'] = data['resourceUser']
            if 'maxPhishingMail' in data and data['maxPhishingMail'] is not None:
                updated_data['max_phishing_mail'] = data['maxPhishingMail']

            # Check if any fields were actually updated
            if not updated_data:
                return handle_response(400, message="No valid updates provided.")

            # Check for existing records with the same values
            existing_query = Training.query.filter(Training.id != id)
            for key, value in updated_data.items():
                if isinstance(value, list):
                    value = ','.join(value)
                existing_query = existing_query.filter(getattr(Training, key) == value)
            
            existing_training = existing_query.first()

            if existing_training:
                return handle_response(409, message="Another training record with these details already exists.")

            # Update the training object
            for key, value in updated_data.items():
                setattr(training, key, value)
            
            update_training_status(training, session)
            # Commit the updates to the database
            session.commit()

            return handle_response(200, message="Training updated successfully")
    
    except IntegrityError as e:
        session.rollback()
        logger.error(f"IntegrityError: {str(e)}")
        return handle_response(400, message="Database integrity error.")

    except Exception as e:
        session.rollback()
        logger.error(f"Exception occurred: {str(e)}")
        return server_error(f"An unexpected error occurred: {str(e)}")

# 여기서 bulk
def handle_res(status_code, data=None, message=None):
    response = {
        "status": status_code,
        "message": message or "No message provided",  # Default message
        "data": data if data is not None else {}  # Ensure JSON serializable structure
    }
    
    return jsonify(response), status_code  # Properly return a JSON response
 

#### Updated `bulk_training` Function
# api/services/training_service.py
from sqlalchemy.exc import SQLAlchemyError

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

def delete_training_serivce(id):
    try:
        with session_scope() as session:
            training = Training.query.get(id)
            if not training:
                return {"error": "Training not found"}, 404
            # 필수 필드만 추출하고, dept_target과 role_target을 적절히 처리
            # training_data = {
            #     'original_id': training.id,
            #     'training_name': training.training_name,
            #     'training_desc': training.training_desc,
            #     'training_start': training.training_start,
            #     'training_end': training.training_end,
            #     'resource_user': training.resource_user,
            #     'max_phishing_mail': training.max_phishing_mail,
            #     'dept_target': training.dept_target,
            #     'role_target': training.role_target
            # }

            # CompleteTraining 인스턴스 생성
            delete_training(training,session)

            session.commit()

            return {"message": "트레이닝이 성공적으로 삭제되었습니다."}, 200

    except ValidationError as err:
        db.session.rollback()
        return {"error": err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": f"트레이닝 삭제 중 오류 발생: {str(e)}"}, 500

    
# 트레이닝 관련 이벤트 로그 조회 함수
def view_training_event_logs(id):
    try:
        event_logs = EventLog.query.filter_by(training_id=id).all()
        return  [t.to_dict() for t in event_logs],200
    except Exception as e:
        return {"error":f"이벤트 로그 조회 중 오류 발생: {str(e)}"}


 

 

def soft_delete_training(id):
    training = Training.query.get(id)
    if not training:
        return {"error": "Training 없음"}, 404

    training.is_deleted = True
    training.deleted_at = datetime.utcnow()  # Use datetime object directly
    db.session.commit()
    return {"message": "Training 논리 삭제"}, 20

 

# Example function for getting random employees.
def get_random_employees(training_id, resource_user_count):
    training = Training.query.get(training_id)
    if training:
        random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
        return [{"id": emp.id, "name": emp.name, "email": emp.email} for emp in random_employees]
    return []
