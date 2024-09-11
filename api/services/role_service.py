from models.role import Role
from api.services.department_service import get_all_departments
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
def validate_training_data(data):
    departments, _ = get_all_departments()
    roles, _ = get_all_roles()
    valid_depts = {dept['code1'] for dept in departments}
    valid_roles = {role['name'] for role in roles}
    
    invalid_depts = set(data.get('deptTarget', [])) - valid_depts
    invalid_roles = set(data.get('roleTarget', [])) - valid_roles
    
    errors = []
    if invalid_depts:
        errors.append(f"Invalid departments: {invalid_depts}")
    if invalid_roles:
        errors.append(f"Invalid roles: {invalid_roles}")
    
    if errors:
        return False, ". ".join(errors)
    return True, None
def get_all_roles():
    try:
        roles = Role.query.all()
        result = [
            {
                "id": role.id,
                "name": role.name,
                "korean_name": role.korean_name
             
            }
            for role in roles
        ]
        return result, 200
    except SQLAlchemyError as e:
        return f"데이터베이스 오류: {str(e)}", 500

def get_role_by_id(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return f"ID가 {role_id}인 역할을 찾을 수 없습니다.", 404
        return {
            "id": role.id,
            "name": role.name,
            "korean_name": role.korean_name
    
        }, 200
    except SQLAlchemyError as e:
        return f"데이터베이스 오류: {str(e)}", 500

def create_new_role(data):
    try:
        if not data or not all(key in data for key in ['name', 'korean_name', 'english_name']):
            return "필수 필드가 누락되었습니다: name, korean_name, english_name", 400

        new_role = Role(**data)
        db.session.add(new_role)
        db.session.commit()
        return {
            "id": new_role.id,
            "name": new_role.name,
            "korean_name": new_role.korean_name
             
        }, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500

def update_role(role_id, data):
    try:
        role = Role.query.get(role_id)
        if not role:
            return f"ID가 {role_id}인 역할을 찾을 수 없습니다.", 404

        for key, value in data.items():
            setattr(role, key, value)

        db.session.commit()
        return {
            "id": role.id,
            "name": role.name,
            "korean_name": role.korean_name 
        }, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500

def delete_role(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return f"ID가 {role_id}인 역할을 찾을 수 없습니다.", 404

        db.session.delete(role)
        db.session.commit()
        return f"ID가 {role_id}인 역할이 삭제되었습니다.", 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"데이터베이스 오류: {str(e)}", 500