from models.department import Department
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import departments_schema ,department_schema,TrainingSchema
from marshmallow import ValidationError
import logging
# 모든 부서 조회
def validate_training_data(data):
    from models.schemas import TrainingSchema
    departments, _ = get_all_departments()
    valid_dept_codes = {dept['code1'].upper() for dept in departments[0] if 'code1' in dept}
    schema = TrainingSchema()
    try:
        validated_data = schema.load(data, context={'valid_dept_codes': valid_dept_codes})
        return validated_data, None
    except ValidationError as e:
        return None, {"error": str(e)}

def get_all_departments():
    try:
        departments = Department.query.all()
        from models.schemas import departments_schema
        return departments_schema.dump(departments), 200
    except SQLAlchemyError as e:
        return {"err": f"데이터베이스 오류: {str(e)}"}, 500


# 새 부서 생성
def create_new_department(data):
    try:
        required_fields = ['name', 'code1', 'code2', 'korean_name']
        if not any(field in data for field in required_fields):
            return {"error": "최소 하나의 필수 필드가 필요합니다"}, 400
        validated_data = department_schema.load(data)
        new_department = Department(**validated_data)
        db.session.add(new_department)
        db.session.commit()
        return department_schema.dump(new_department), 201
    except ValidationError as e:
        return {"error": str(e)}, 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"데이터베이스 오류: {str(e)}"}, 500

# ID로 부서 조회
def get_department_by_id(department_id):
    try:
        department = Department.query.get(department_id)
        if not department:
            return {"error": f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다."}, 404
        return department_schema.dump(department), 200
    except SQLAlchemyError as e:
        return {"error": f"데이터베이스 오류: {str(e)}"}, 500

# 부서 정보 업데이트
def update_department(department_id, data):
    try:
        department = Department.query.get(department_id)
        if not department:
            return {"err":f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다."}, 404

        validated_data=department_schema.load(data, partial=True)
        for key, value in data.items():
            setattr(department, key, value)
        
        db.session.commit()
        return department_schema.dump(department),200
    except ValidationError as e:
        return {"error": str(e)}, 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return{"error": f"데이터베이스 오류: {str(e)}"}, 500

# 부서 삭제
def delete_department(department_id):
    try:
        department = Department.query.get(department_id)
        if not department:
            return {"error": f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다."}, 404

        db.session.delete(department)
        db.session.commit()
        return {"message":"부서가 성공적으로 삭제되었습니다."}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error":f"데이터베이스 오류: {str(e)}"}, 500

#  