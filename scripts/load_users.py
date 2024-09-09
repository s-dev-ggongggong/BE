import os,sys ,time, bcrypt ,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from run import create_app,db
from models.role import Role
from models.department import Department
from models.employee import Employee
from sqlalchemy.exc import OperationalError ,IntegrityError
from extensions import session_scope
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']
    
def load_json(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)
    

def load_roles(session):
    roles = [
        "인턴", "사원", "주임", "계장", "대리", "과장", "차장", "부장", "감사",
        "이사", "상무", "전무", "부사장", "사장", "임원",
        "연구원", "주임연구원", "선임연구원", "책임연구원", "수석연구원", "연구소장"
    ]
    for role_name in roles:
        existing_role = session.query(Role).filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            session.add(role)

    session.commit()
    print("Roles have been populated.")
def load_departments(session):
    departments = [
        "Engineering", "Marketing", "Sales", "Human Resources", "Research and Development"
    ]

    for dept_name in departments:
        existing_department = session.query(Department).filter_by(name=dept_name).first()
        if not existing_department:
            department = Department(name=dept_name)
            session.add(department)

    session.commit()
    print("Departments have been populated.")

def load_users():
    app=create_app()
    with app.app_context():
        with session_scope() as session:
            load_roles(session)
            load_departments(session)
            users_data = load_json('static/users.json') 
            #with db.session.no_autoflush:
                        
            for user_data in users_data:
       
                retries=5
                while retries>0:
                    try:
                        if not Employee.query.filter_by(email=user_data['email']).first():
                            role = session.query(Role).filter_by(name=user_data['role_name']).first()
                            if not role:
                                print(f"Role {user_data['role_name']} not found for user {user_data['email']}")
                                break
                            department =session.query(Department).filter_by(name=user_data['department']).first()
                            if not department:
                                print(f"Department {user_data['department']} not found for user {user_data['email']}")
                                break

                            user = Employee(
                                username=user_data['username'],
                                email=user_data['email'],
                                password=user_data['password'],  
                                department_id=department.id,
                                role_id=role.id 
                            )

                            session.add(user)
                            session.commit()

                            print(f"Added user: {user_data['email']}")
                        else:
                            print(f"{user_data['email']} exists!")
                        break
                    except IntegrityError :
                        print(f"IntegrityError {user_data['email']} exist!")
                        session.rollback()
                    
                    except OperationalError as e :
                        if "database is locked" in str(e):
                            retries -=1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise
if __name__ == "__main__":
    load_users()
    print("Database populated successfully!")