from models.department import Department
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

# 모든 부서 조회
def get_all_departments():
    try:
        departments = Department.query.all()
        result = [
            {
                "id": department.id, 
                "name": department.name, 
                "code1": department.code1, 
                "code2": department.code2, 
                "korean_name": department.korean_name
            } 
            for department in departments
        ]
        return result, 200
    except SQLAlchemyError as e:
        return f"데이터베이스 오류: {str(e)}", 500

# 새 부서 생성
def create_new_department(data):
    try:
        if not data or not data.get('name'):
            return "부서 이름은 필수 입력 항목입니다.", 400
        
        new_department = Department(**data)
        db.session.add(new_department)
        db.session.commit()

        return {
            "id": new_department.id, 
            "name": new_department.name
        }, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500

# ID로 부서 조회
def get_department_by_id(department_id):
    try:
        department = Department.query.get(department_id)
        if not department:
            return f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다.", 404
        
        return {
            "id": department.id, 
            "name": department.name, 
            "code1": department.code1, 
            "code2": department.code2, 
            "korean_name": department.korean_name
        }, 200
    except SQLAlchemyError as e:
        return f"데이터베이스 오류: {str(e)}", 500

# 부서 정보 업데이트
def update_department(department_id, data):
    try:
        department = Department.query.get(department_id)
        if not department:
            return f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다.", 404

        for key, value in data.items():
            setattr(department, key, value)
        
        db.session.commit()
        return {
            "id": department.id, 
            "name": department.name
        }, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500

# 부서 삭제
def delete_department(department_id):
    try:
        department = Department.query.get(department_id)
        if not department:
            return f"ID {department_id}에 해당하는 부서를 찾을 수 없습니다.", 404

        db.session.delete(department)
        db.session.commit()
        return "부서가 성공적으로 삭제되었습니다.", 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500

# 부서와 역할 정보 조회
def get_departments_with_roles():
    try:
        departments = Department.query.all()
        result = [
            {
                "id": department.id,
                "name": department.name,
                "code1": department.code1,
                "code2": department.code2,
                "korean_name": department.korean_name,
                "roles": [role.name for role in department.roles]
            }
            for department in departments
        ]
        return result, 200
    except SQLAlchemyError as e:
        return f"데이터베이스 오류: {str(e)}", 500