from api.services.department_service import get_all_departments
from api.services.role_service import get_all_roles
from models.schemas import TrainingSchema ,training_schema, complete_training_schema
from models.init import Training, EventLog, Employee ,CompleteTraining

from extensions import db
from utils.api_error_handlers import validate_training_data
from marshmallow import ValidationError
from flask import jsonify, request
from datetime import datetime
from sqlalchemy.sql import func
import logging

def validate_training_data(data,valid_depts, valid_roles):
 
    invalid_depts = set(data.get('deptTarget', [])) - valid_depts
    invalid_roles = set(data.get('roleTarget', [])) - valid_roles
 
    if invalid_depts or invalid_roles:
        return False, f"Invalid departments: {invalid_depts}, Invalid roles: {invalid_roles}",400
    return True, None

# 트레이닝 생성 함수

def create_training(data):
    try:
        if not data:
            return {"error": "요청 본문이 비어있습니다."}, 400
        
        departments, _ = get_all_departments()
        roles, _ = get_all_roles()
        valid_depts = {dept['code1'] for dept in departments}
        valid_roles = {role['name'] for role in roles}

        errors = validate_training_data(data, valid_depts, valid_roles)
        if errors:
            return {"error": errors}, 400
        
        existing_training = Training.query.filter_by(
            training_name=data["trainingName"],
            training_desc=data["trainingDesc"],
            training_start=data["trainingStart"],
            training_end=data["trainingEnd"],
        ).first()

        if existing_training:
            return {"error": "동일한 트레이닝이 이미 존재합니다."}, 400


        training_schema = TrainingSchema()
        try:
            new_training = training_schema.load(data)
        except ValidationError as e:
            return {"error": e.messages}, 400

        db.session.add(new_training)
        db.session.commit()

        result = training_schema.dump(new_training)
        return result, 201


    except ValidationError as e:
        return {"error": f"Validation failed: {e.messages}"}, 400
    except Exception as e:
        logging.exception("Unexpected error in create_training")
        return {"error": f"트레이닝 생성 중 오류 발생: {str(e)}"}, 500



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
from datetime import datetime

def update_training_service(id, data):
    
    try:        
        existing_training =Training.query.get(id)
        if existing_training and existing_training.id != id:
            return {"error": "동일한 트레이닝이 이미 존재합니다."}, 400

   
        if data.get('status') == 'fin':
            complete_training(id)
            
        
 
        # Fetch the training by ID
        training = Training.query.get(id)
        if not training:
            return {"message": "Training not found"}, 404

        for k, v in data.items():
            if hasattr(training,k) and v is not None:
                setattr(training,k,v)
        db.session.commit()
        return {"message": "Training업 데이트 성공", "training": training.to_dict()}  
    except Exception as e:
        return  {"error": f"트레이닝 업데이트 중 오류 발생: {str(e)}"}, 500

def delete_training(id):
    try:
        training = Training.query.get_or_404(id)
        training_data = training_schema.dump(training)
        training_data['original_id'] = training_data.pop('id')

        deleted_training = complete_training_schema.load(training_data)

        db.session.add(deleted_training)
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
        return {"error": "요청 본문이 비어있습니다."}, 400
    
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
    training = Training.query.get(training_id)
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

def soft_delete_training(id):
    training = Training.query.get(id)
    if not training:
        return {"error": "Training 없음"}, 404

    training.is_deleted = True
    training.deleted_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return {"message": "Training 논리 삭제 "}, 200

 


def get_random_employees(training_id, resource_user_count):
    # 랜덤으로 지정된 수의 직원을 선택하는 쿼리
    training = Training.query.get(training_id)
    random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
    return [{"id": emp.id, "name": emp.name, "email": emp.email} for emp in random_employees]

