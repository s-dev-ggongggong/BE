import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from app import create_app
from extensions import db
from models.employee import Employee
from scripts.utils import load_json

def load_employees(file_path):
    app = create_app()
    with app.app_context():
        # Clear existing employees
        Employee.query.delete()
        db.session.commit()

        data = load_json(file_path)
        for item in data:
            if item['email'] == 'admin@ip-10-0-10-162.ap-northeast-2.compute.internal':
                # Special handling for ADMIN user
                employee = Employee(
                    name=item['name'],
                    email=item['email'],
                    password=item['password'],
                    role_name=item['role_name'],
                    department_name=item['department_name'],
                    admin_id='admin',
                    admin_pw='admin1234'
                )
            else:
                # For non-admin users
                employee = Employee(
                    name=item['name'],
                    email=item['email'],
                    password=item['password'],
                    role_name=item['role_name'],
                    department_name=item['department_name'],
                    admin_id=None,
                    admin_pw=None
                )
            db.session.add(employee)
        db.session.commit()

if __name__ == '__main__':
    load_employees('data/employees.json')