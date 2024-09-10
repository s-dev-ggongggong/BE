import os, sys, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from init import create_app
from models.role import Role
from utils.db_error_handlers import handle_db_errors
from models.department import Department
from models.employee import Employee
from sqlalchemy.exc import OperationalError, IntegrityError
from extensions import session_scope, db
import chardet

# Detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# Load JSON data with detected encoding
def load_json(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

@handle_db_errors
# Load user data and map roles without hardcoded mappings
def load_users():
    app = create_app()
    with app.app_context():
        with session_scope() as session:
            users_data = load_json('static/users.json')
            print(f"Loaded {len(users_data)} users from JSON.")  # 사용자 데이터 로드 확인
            
            for user_data in users_data:
                retries = 5
                while retries > 0:
                    try:
                        print(f"Processing user: {user_data['email']}")
                        
                        # 이메일로 사용자 조회
                        existing_user = Employee.query.filter_by(email=user_data['email']).first()
                        if existing_user:
                            print(f"User {user_data['email']} already exists!")
                            break

                        role_name_key = user_data.get('roleName')

                        # 영어 이름으로 역할 조회
                        role = session.query(Role).filter_by(name=role_name_key).first()

                        # 한글 이름으로 역할 조회
                        if not role:
                            print(f"Role {role_name_key} not found by English name, trying Korean name...")
                            role = session.query(Role).filter_by(korean_name=role_name_key).first()

                        if not role:
                            print(f"Role {role_name_key} not found for user {user_data['email']}")
                            break

                        print(f"Found role: {role.name} ({role.korean_name}) for user {user_data['email']}")

                        # 부서 조회
                        department = session.query(Department).filter_by(name=user_data['department']).first()
                        if not department:
                            print(f"Department {user_data['department']} not found for user {user_data['email']}")
                            break

                        print(f"Found department: {department.name} for user {user_data['email']}")

                        # 사용자 추가
                        user = Employee(
                            name=user_data['name'],
                            email=user_data['email'],
                            password="igloo1234",  # Fixed password
                            department_id=department.id,
                            role_id=role.id  # 매칭된 역할의 ID 사용
                        )

                        session.add(user)
                        session.commit()
                        print(f"Added user: {user_data['email']}")
                        break
                        
                    except IntegrityError as ie:
                        print(f"IntegrityError for user {user_data['email']}: {str(ie)}")
                        session.rollback()
                        break
                        
                    except OperationalError as oe:
                        if "database is locked" in str(oe):
                            retries -= 1
                            print(f"Database is locked, retrying... ({retries} retries left)")
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            print(f"OperationalError: {str(oe)}")
                            raise

if __name__ == "__main__":
    load_users()
    print("Database populated successfully!")
