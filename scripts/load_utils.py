import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from models.event_log import EventLog

# Setup paths

from datetime import datetime
from flask import Flask
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from config import Config
 

  

def camel_to_snake(name):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)