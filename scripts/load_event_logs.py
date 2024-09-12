import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.event_log import EventLog
import json
from datetime import datetime
from models.event_log import EventLog
from extensions import db
from app import create_app

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Loaded {len(data)} items from {file_path}")
    return data

def process_events(events_data):
    return [{
        'action': event['action'],
        'timestamp': datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S'),
        'training_id': event['trainingId'],
        'message': event['message']
    } for event in events_data]


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.event_log import EventLog
import json
from datetime import datetime
from models.event_log import EventLog
from extensions import db
from app import create_app

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Loaded {len(data)} items from {file_path}")
    return data

def process_events(events_data):
    return [{
        'action': event['action'],
        'timestamp': datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S'),
        'training_id': event['trainingId'],
        'message': event['message']
    } for event in events_data]


def load_event(file_path):
     app = create_app()
     with app.app_context():
       with db.session.begin():
           events_data = load_json(file_path)
           for event_data in process_events(events_data):
               db.session.add(EventLog(**event_data))
       print(f"Loaded {len(events_data)} events")


if __name__ == '__main__':
    load_event('data/event_logs.json')
 