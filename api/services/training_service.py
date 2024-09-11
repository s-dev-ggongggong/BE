from api.services.department_service import get_all_departments
from api.services.role_service import get_all_roles
from models.schemas import TrainingSchema ,training_schema,deleted_training_schema
from models.init import Training, EventLog, Employee ,DeletedTraining

from extensions import db
from utils.api_error_handlers import validate_training_data
from marshmallow import ValidationError

from datetime import datetime
from sqlalchemy.sql import func
import logging

def validate_training_data(data):
    print(f"Validation Data: {data}")
    departments, _ = get_all_departments()
    roles, _ = get_all_roles()
    valid_depts = {dept['code1'] for dept in departments}
    valid_roles = {role['name'] for role in roles}
    
    invalid_depts = set(data.get('deptTarget', [])) - valid_depts
    invalid_roles = set(data.get('roleTarget', [])) - valid_roles
    
    if invalid_depts or invalid_roles:
        return False, f"Invalid departments: {invalid_depts}, Invalid roles: {invalid_roles}"
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

        invalid_depts = set(data.get('deptTarget', [])) - valid_depts
        invalid_roles = set(data.get('roleTarget', [])) - valid_roles

        if invalid_depts or invalid_roles:
            error_message = {}
            if invalid_depts:
                error_message["deptTarget"] = f"Invalid departments: {invalid_depts}"
            if invalid_roles:
                error_message["roleTarget"] = f"Invalid roles: {invalid_roles}"
            return {"error": error_message}, 400
        
        existing_training = Training.query.filter_by(
            training_name=data["trainingName"],
            training_desc=data["trainingDesc"],
            training_start=data["trainingStart"],
            training_end=data["trainingEnd"],
            resource_user=data["resourceUser"],
            max_phishing_mail=data["maxPhishingMail"],
            dept_target=','.join(data["deptTarget"]),
            role_target=','.join(data["roleTarget"])
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
        return [t.to_dict() for t in trainings], 200 
    except Exception as e:
        return {"error":f"트레이닝 조회 중 오류 발생: {str(e)}"},500

# 특정 트레이닝 조회 함수
def get_training(id):
    try:
        training = Training.query.get_or_404(id)
        return training.to_dict(), 200
    except Exception as e:
        return {"error":f"트레이닝 조회 중 오류 발생: {str(e)}"},404

# 트레이닝 업데이트 함수
from datetime import datetime

def update_training_service(id, data):
    print(f"Received ID: {id}")
    print(f"Received Data: {data}")

    try:
        # 중복 검사 추가
        existing_training = Training.query.filter_by(training_name=data.get('trainingName')).first()
        if existing_training and existing_training.id != id:
            return {"error": "동일한 트레이닝이 이미 존재합니다."}, 400

        # Fetch the training by ID
        training = Training.query.get(id)
        if not training:
            return {"message": "Training not found"}, 404

        updated = False

        # 각 필드별로 값이 전달된 경우에만 업데이트
        if 'trainingName' in data:
            if not data['trainingName']:
                return {"error": "trainingName 필드는 비어있을 수 없습니다."}, 400
            if training.training_name != data['trainingName']:
                print(f"Updating training_name from {training.training_name} to {data['trainingName']}")
                training.training_name = data['trainingName']
                updated = True

        if 'trainingDesc' in data:
            if not data['trainingDesc']:
                return {"error": "trainingDesc 필드는 비어있을 수 없습니다."}, 400
            if training.training_desc != data['trainingDesc']:
                print(f"Updating training_desc from {training.training_desc} to {data['trainingDesc']}")
                training.training_desc = data['trainingDesc']
                updated = True

        if 'trainingStart' in data:
            if not data['trainingStart']:
                return {"error": "trainingStart 필드는 비어있을 수 없습니다."}, 400
            training_start_date = datetime.strptime(data['trainingStart'], "%Y-%m-%d").date()
            if training.training_start != training_start_date:
                print(f"Updating training_start from {training.training_start} to {training_start_date}")
                training.training_start = training_start_date
                updated = True

        if 'trainingEnd' in data:
            if not data['trainingEnd']:
                return {"error": "trainingEnd 필드는 비어있을 수 없습니다."}, 400
            training_end_date = datetime.strptime(data['trainingEnd'], "%Y-%m-%d").date()
            if training.training_end != training_end_date:
                print(f"Updating training_end from {training.training_end} to {training_end_date}")
                training.training_end = training_end_date
                updated = True

        if 'resourceUser' in data:
            if not data['resourceUser']:
                return {"error": "resourceUser 필드는 비어있을 수 없습니다."}, 400
            if training.resource_user != data['resourceUser']:
                print(f"Updating resource_user from {training.resource_user} to {data['resourceUser']}")
                training.resource_user = data['resourceUser']
                updated = True

        if 'maxPhishingMail' in data:
            if not data['maxPhishingMail']:
                return {"error": "maxPhishingMail 필드는 비어있을 수 없습니다."}, 400
            if training.max_phishing_mail != data['maxPhishingMail']:
                print(f"Updating max_phishing_mail from {training.max_phishing_mail} to {data['maxPhishingMail']}")
                training.max_phishing_mail = data['maxPhishingMail']
                updated = True

        if 'deptTarget' in data:
            if not data['deptTarget'] or not data['deptTarget'][0]:
                return {"error": "deptTarget 필드는 비어있을 수 없습니다."}, 400
            new_dept_target = ','.join(data['deptTarget'])
            if training.dept_target != new_dept_target:
                print(f"Updating dept_target from {training.dept_target} to {new_dept_target}")
                training.dept_target = new_dept_target
                updated = True

        if 'roleTarget' in data:
            if not data['roleTarget'] or not data['roleTarget'][0]:
                return {"error": "roleTarget 필드는 비어있을 수 없습니다."}, 400
            new_role_target = ','.join(data['roleTarget'])
            if training.role_target != new_role_target:
                print(f"Updating role_target from {training.role_target} to {new_role_target}")
                training.role_target = new_role_target
                updated = True

        # 업데이트 사항이 있다면 커밋
        if updated:
            db.session.commit()
            print(f"Training ID {id} successfully updated.")
            return {"message": "Training updated successfully", "training": training.to_dict()}, 200
        else:
            return {"message": "No changes detected"}, 200

    except Exception as e:
        return {"error": f"트레이닝 업데이트 중 오류 발생: {str(e)}"}, 500
    
def delete_training(id):
    try:
        training = Training.query.get_or_404(id)
        training_data = training_schema.dump(training)
        training_data['original_id'] = training_data.pop('id')

        deleted_training = deleted_training_schema.load(training_data)

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
    try:
        if not data:
            return {"error": "요청 본문이 비어있습니다."}, 400
        
        trainings = []
        duplicate_trainings = []
        invalid_trainings = []
        
        training_schema = TrainingSchema()
        
        for training_data in data:
            try:
                validated_data = training_schema.load(training_data)  # 각 트레이닝 데이터 검증
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
                    continue  # Skip adding duplicates to the trainings list
                new_training = Training(**validated_data)
                trainings.append(new_training)  # Add valid training
            except ValidationError as e:
                invalid_trainings.append({"error": str(e.messages), "data": training_data})
                continue
        
        if trainings:
            db.session.add_all(trainings)
            db.session.commit()

        response = {
            "message": "Bulk training 성공",
            "valid_trainings": [t.to_dict() for t in trainings],
            "duplicate_trainings": duplicate_trainings,
            "invalid_trainings": invalid_trainings
        }
        return response, 201
    
    except Exception as e:
        return {"error": f"벌크 트레이닝 생성 중 오류 발생: {str(e)}"}# email 연동 decopuling
# File: services/training_service.py
 


 


def get_random_employees(training_id, resource_user_count):
    # 랜덤으로 지정된 수의 직원을 선택하는 쿼리
    training = Training.query.get(training_id)
    random_employees = Employee.query.order_by(func.random()).limit(resource_user_count).all()
    return [{"id": emp.id, "name": emp.name, "email": emp.email} for emp in random_employees]

