import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   
import json
from datetime import datetime

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def parse_datetime(value):
    if isinstance(value, str):
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value