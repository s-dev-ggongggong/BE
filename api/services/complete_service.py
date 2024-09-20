from models.department import Department
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import departments_schema ,department_schema,TrainingSchema
from marshmallow import ValidationError
import logging