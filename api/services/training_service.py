 
from models.schemas import TrainingSchema ,training_schema
from models.init import Training, EventLog, Employee ,CompleteTraining

from extensions import db

from marshmallow import ValidationError
from flask import jsonify
from datetime import datetime
from sqlalchemy.sql import func
import logging

from sqlalchemy.exc import IntegrityError
from flask import jsonify
import json
import logging
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
# 트레이닝 생성 함수


def create_training_service(data):
    try:
        # JSON 데이터에서 필요한 필드 추출 및 매핑
        mapped_data = {
            'training_name': data.get('trainingName'),
            'training_desc': data.get('trainingDesc'),
            'training_start': convert_date_string_to_datetime(data.get('trainingStart')),
            'training_end': convert_date_string_to_datetime(data.get('trainingEnd')),
            'dept_target': data.get('deptTarget', []),  # JSON encoding handled by JSONEncodedDict
            'role_target': data.get('roleTarget', []),  # JSON encoding handled by JSONEncodedDict
            'max_phishing_mail': data.get('maxPhishingMail'),
            'resource_user': data.get('resourceUser')
        }

        logging.info(f"Mapped data: {mapped_data}")

        # Check for existing records with the same values
        existing_training = Training.query.filter_by(
            training_name=mapped_data['training_name'],
            training_desc=mapped_data['training_desc'],
            training_start=mapped_data['training_start'],
            training_end=mapped_data['training_end'],
            max_phishing_mail=mapped_data['max_phishing_mail'],
            resource_user=mapped_data['resource_user'],
            dept_target=mapped_data['dept_target'],
            role_target=mapped_data['role_target']
        ).first()

        if existing_training:
            return jsonify({"error": "A training record with these details already exists."}), 409

        # Training 객체 생성 및 데이터베이스에 저장
        new_training = Training(**mapped_data)
        db.session.add(new_training)
        db.session.commit()

        # 성공적으로 저장된 데이터를 반환
        response_data = training_schema.dump(new_training)
        return jsonify({'message': 'Training created successfully', 'data': response_data}), 201

    except IntegrityError as e:
        logging.error(f"IntegrityError: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
 
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
 

from sqlalchemy.exc import IntegrityError
import json
 

from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify

from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify


from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify



from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify, Response

from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify

from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify, Response

from sqlalchemy.exc import IntegrityError
import json
from flask import jsonify


def update_training_service(id, data):
    try:
        training = Training.query.get(id)
        if not training:
            return {"message": "Training not found"}, 404
        
        new_dept_target = data.get('deptTarget', training.dept_target)
        new_role_target = data.get('roleTarget', training.role_target)
        
        new_training_start = convert_date_string_to_datetime(data.get('trainingStart', training.training_start.strftime('%Y-%m-%d %H:%M:%S')))
        new_training_end = convert_date_string_to_datetime(data.get('trainingEnd', training.training_end.strftime('%Y-%m-%d %H:%M:%S')))

        if (new_dept_target == training.dept_target and
            new_role_target == training.role_target and
            data.get('trainingName', training.training_name) == training.training_name and
            data.get('trainingDesc', training.training_desc) == training.training_desc and
            new_training_start == training.training_start and
            new_training_end == training.training_end and
            data.get('resourceUser', training.resource_user) == training.resource_user and
            data.get('maxPhishingMail', training.max_phishing_mail) == training.max_phishing_mail):
            return {"message": "No changes detected"}, 200

        duplicate_training = Training.query.filter(
            Training.training_name == data.get('trainingName'),
            Training.training_desc == data.get('trainingDesc'),
            Training.training_start == new_training_start,
            Training.training_end == new_training_end
        ).first()

        if duplicate_training and duplicate_training.id != id:
            return {"error": "Duplicate training found"}, 400

        training.dept_target = new_dept_target
        training.role_target = new_role_target
        training.training_name = data.get('trainingName', training.training_name)
        training.training_desc = data.get('trainingDesc', training.training_desc)
        training.training_start = new_training_start
        training.training_end = new_training_end
        training.resource_user = data.get('resourceUser', training.resource_user)
        training.max_phishing_mail = data.get('maxPhishingMail', training.max_phishing_mail)
        
        db.session.commit()

        return {"message": "Training updated successfully"}, 200

    except IntegrityError:
        db.session.rollback()
        return {"error": "Database integrity error"}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


    

def delete_training(id):
    try:
        training = Training.query.get_or_404(id)

        # 필수 필드만 추출하고, dept_target과 role_target을 적절히 처리
        training_data = {
            'original_id': training.id,
            'training_name': training.training_name,
            'training_desc': training.training_desc,
            'training_start': training.training_start,
            'training_end': training.training_end,
            'resource_user': training.resource_user,
            'max_phishing_mail': training.max_phishing_mail,
            'dept_target': training.dept_target,
            'role_target': training.role_target
        }

        # CompleteTraining 인스턴스 생성
        deleted_training = CompleteTraining(**training_data)

        # CompleteTraining 테이블에 추가
        db.session.add(deleted_training)

        # 기존 Training 데이터 삭제
        db.session.delete(training)
        db.session.commit()

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
        return result.to_dict() ,200
    except Exception as e:
        return {"error":f"사용자 필터링 중 오류 발생: {str(e)}"}


# 벌크 트레이닝 생성 함수
def bulk_training(data):
    if not data:
        return {"error": "요청 본문이 비어있습니다."}, 409
    
    trainings = []
    duplicate_trainings = []
    invalid_trainings = []
    
    for training_data in data:
            try:
                validated_data = TrainingSchema.load(training_data)  # 각 트레이닝 데이터 검증
                existing_training = Training.query.filter_by(
                    training_name=validated_data["training_name"],
                    training_desc=validated_data["training_desc"],
                    training_start=validated_data["training_start"],
                    training_end=validated_data["training_end"]
                ).first()

                if existing_training:
                    duplicate_trainings.append({
                        "training_name": validated_data["training_name"],
                        "training_id": existing_training.id
                    })
                else:
                    trainings.append(Training(**validated_data))  # Add valid training
            except ValidationError as e:
                invalid_trainings.append({"error": str(e.messages), "data": training_data})
        
    if trainings:
        db.session.add_all(trainings)
        db.session.commit()

    return {
            "message": "Bulk training 성공",
            "valid_trainings": [t.to_dict() for t in trainings],
            "duplicate_trainings": duplicate_trainings,
            "invalid_trainings": invalid_trainings
        },201

def complete_training(training_id):
    training = Training.query.with_deleted().filter_by(id=training_id).first()
    
    if training:
        complete = CompleteTraining(
            original_id=training.id,
            training_name=training.training_name,
            training_desc=training.training_desc,
            training_start=training.training_start,
            training_end=training.training_end,
            resource_user=training.resource_user,
            max_phishing_mail=training.max_phishing_mail,
            dept_target=training.dept_target,
            role_target=training.role_target,
            completed_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(complete)
        db.session.commit()

from datetime import datetime

def soft_delete_training(id):
    training = Training.query.get(id)
    if not training:
        return {"error": "Training 없음"}, 404

    training.is_deleted = True
    training.deleted_at = datetime.utcnow()  # Use datetime object directly
    db.session.commit()
    return {"message": "Training 논리 삭제"}, 20

 

def get_random_employees(training_id, resource_user_count):
    # 랜덤으로 지정된 수의 직원을 선택하는 쿼리
    training = Training.query.get(training_id)
    if training:
        random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
        return [{"id": emp.id, "name": emp.name, "email": emp.email} for emp in random_employees]
    return []
