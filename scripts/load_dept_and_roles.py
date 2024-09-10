import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from flask import Flask
from extensions import db
from models.department import Department
from models.role import Role
from models.auth_token import AuthToken
from models.employee import Employee
from models.event_log import EventLog
from utils.db_error_handlers import handle_db_errors

# ... (나머지 코드 유지)

from utils.db_error_handlers import handle_db_errors

def create_minimal_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    return app

app = create_minimal_app()

@handle_db_errors   
def upload_departments_and_roles():
        with app.app_context():
            departments_with_roles = [
            {
                "name": "Human Resources",
                "code1": "HR",
                "code2": "HUMAN_RESOURCES",
                "korean_name": "인사부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "HR_SPECIALIST", "korean_name": "HR 전문가"},
                    {"english_name": "HR_MANAGER", "korean_name": "HR 관리자"}
                ]
            },
            {
                "name": "Information Technology",
                "code1": "IT",
                "code2": "IT_DEPARTMENT",
                "korean_name": "정보기술부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "SYSTEM_ADMIN", "korean_name": "시스템 관리자"},
                    {"english_name": "DEVELOPER", "korean_name": "개발자"},
                    {"english_name": "SENIOR_DEVELOPER", "korean_name": "선임 개발자"},
                    {"english_name": "TECHNICAL_LEAD", "korean_name": "기술 리더"},
                    {"english_name": "IT_MANAGER", "korean_name": "IT 관리자"}
                ]
            },
            {
                "name": "Finance",
                "code1": "FN",
                "code2": "FINANCE_DEPARTMENT",
                "korean_name": "재무부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "ACCOUNTANT", "korean_name": "회계사"},
                    {"english_name": "FINANCIAL_ANALYST", "korean_name": "재무 분석가"},
                    {"english_name": "FINANCE_MANAGER", "korean_name": "재무 관리자"},
                    {"english_name": "CONTROLLER", "korean_name": "통제자"}
                ]
            },
            {
                "name": "Marketing",
                "code1": "MK",
                "code2": "MARKETING_DEPARTMENT",
                "korean_name": "마케팅부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "MARKETING_SPECIALIST", "korean_name": "마케팅 전문가"},
                    {"english_name": "BRAND_MANAGER", "korean_name": "브랜드 관리자"},
                    {"english_name": "MARKETING_ANALYST", "korean_name": "마케팅 분석가"},
                    {"english_name": "MARKETING_MANAGER", "korean_name": "마케팅 관리자"}
                ]
            },
            {
                "name": "Sales",
                "code1": "SL",
                "code2": "SALES_DEPARTMENT",
                "korean_name": "영업부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "SALES_REPRESENTATIVE", "korean_name": "영업 대표"},
                    {"english_name": "ACCOUNT_MANAGER", "korean_name": "계정 관리자"},
                    {"english_name": "SALES_MANAGER", "korean_name": "영업 관리자"},
                    {"english_name": "REGIONAL_SALES_DIRECTOR", "korean_name": "지역 영업 이사"}
                ]
            },
            {
                "name": "Research and Development",
                "code1": "RD",
                "code2": "RESEARCH_DEVELOPMENT",
                "korean_name": "연구개발부",
                "roles": [
                    {"english_name": "INTERN", "korean_name": "인턴"},
                    {"english_name": "EMPLOYEE", "korean_name": "사원"},
                    {"english_name": "SENIOR_CLERK", "korean_name": "주임"},
                    {"english_name": "ASSISTANT_MANAGER", "korean_name": "계장"},
                    {"english_name": "MANAGER", "korean_name": "대리"},
                    {"english_name": "DEPUTY_GENERAL_MANAGER", "korean_name": "과장"},
                    {"english_name": "GENERAL_MANAGER", "korean_name": "차장"},
                    {"english_name": "DIRECTOR", "korean_name": "부장"},
                    {"english_name": "RESEARCHER", "korean_name": "연구원"},
                    {"english_name": "SENIOR_RESEARCHER", "korean_name": "선임 연구원"},
                    {"english_name": "PRINCIPAL_RESEARCHER", "korean_name": "주임 연구원"},
                    {"english_name": "CHIEF_RESEARCHER", "korean_name": "책임 연구원"},
                    {"english_name": "SENIOR_CHIEF_RESEARCHER", "korean_name": "수석 책임 연구원"},
                    {"english_name": "RESEARCH_DIRECTOR", "korean_name": "연구소장"}
                ]
            }
        ]
            with app.app_context():
                for dept_data in departments_with_roles:
                    department = Department.query.filter_by(code1=dept_data["code1"]).first()
                    if department:
                        print(f"Updating department: {dept_data['name']}")
                        department.name = dept_data["name"]
                        department.code2 = dept_data["code2"]
                        department.korean_name = dept_data["korean_name"]
                    else:
                        print(f"Inserting new department: {dept_data['name']}")
                        department = Department(
                            name=dept_data["name"],
                            code1=dept_data["code1"],
                            code2=dept_data["code2"],
                            korean_name=dept_data["korean_name"]
                        )
                        db.session.add(department)
                        db.session.flush()

                    for role_data in dept_data["roles"]:
                        role = Role.query.filter_by(name=role_data["english_name"]).first()

                        if role:
                            if role.korean_name != role_data["korean_name"]:
                                print(f"Updating korean_name for role: {role.name}")
                                role.korean_name = role_data["korean_name"]
                                print(f"Updated korean_name: {role.korean_name} for role: {role.name}")
                                db.session.add(role)
                        else:
                            print(f"Inserting new role: {role_data['english_name']} - {role_data['korean_name']}")
                            role = Role(
                                name=role_data["english_name"],
                                korean_name=role_data["korean_name"]
                            )
                            db.session.add(role)
                            print(f"Inserted new role: {role.name} with korean_name: {role.korean_name}")

                        db.session.flush()

                        dept_role = DepartmentRole.query.filter_by(department_id=department.id, role_id=role.id).first()
                        if not dept_role:
                            dept_role = DepartmentRole(department_id=department.id, role_id=role.id)
                            db.session.add(dept_role)

                db.session.commit()
                print("Departments and roles have been updated/inserted successfully.")

if __name__ == "__main__":
    with app.app_context():    
        upload_departments_and_roles()
        print("Departments and roles loaded successfully!")
    db.configure_mappers()