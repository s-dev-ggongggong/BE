from models.employee import Employee
from models.role import Role
from models.department import Department
from extensions import db
from werkzeug.security import generate_password_hash

def create_admin():
    admin_role = Role.query.filter_by(name="IT 관리자").first()
    if not admin_role:
        admin_role = Role(name="IT 관리자", korean_name="IT 관리자")
        db.session.add(admin_role)

    admin_dept = Department.query.filter_by(name="정보기술부").first()
    if not admin_dept:
        admin_dept = Department(name="정보기술부", code="IT")
        db.session.add(admin_dept)

    admin = Employee.query.filter_by(email="admin@ip-10-0-10-162.ap-northeast-2.compute.internal").first()
    if not admin:
        admin = Employee(
            name="ADMIN",
            email="admin@ip-10-0-10-162.ap-northeast-2.compute.internal",
            password=generate_password_hash("admin1234"),
            role_id=admin_role.id,
            department_id=admin_dept.id,
            is_admin=True
        )
        db.session.add(admin)

    db.session.commit()

# 애플리케이션 시작 시 실행
create_admin()