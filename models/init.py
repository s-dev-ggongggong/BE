from models.department import Department
from models.role import Role
from models.employee import Employee
from models.auth_token import AuthToken
from models.training import Training
from models.email import Email
from models.delete_train import DeletedTraining
from models.event_log import EventLog
__all__ = [
    'Department', 'Role', 'Employee',    'AuthToken',  
 'Training', 'Email', 'EventLog' ,'DeletedTraining'
 
]