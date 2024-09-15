import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from scripts.load_trainings import load_trainings
from scripts.load_roles import load_roles
from scripts.load_departments import load_departments
from scripts.load_emails import load_emails
from scripts. load_employees import load_employees
if __name__ == '__main__':
    load_departments('data/departments.json')
    load_roles('data/roles.json')
    load_trainings('data/trainings.json')
    load_emails('data/emails.json')
    load_employees('data/employees.json')