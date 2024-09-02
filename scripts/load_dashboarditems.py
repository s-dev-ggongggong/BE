import json,os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

from datetime import datetime
from run import create_app, db
from models.dashboard import DashboardItem
from sqlalchemy.exc import OperationalError, IntegrityError
from extensions import session_scope

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_dashboard_items():
    app = create_app()
    with app.app_context():
        with session_scope() as session:
            # Load dashboard item data from dashboard_items.json
            dashboard_items_data = load_json('static/dashboard_items.json')

            for item_data in dashboard_items_data:
                retries = 5
                while retries > 0:
                    try:
                        item = DashboardItem(
                            title=item_data['title'],
                            value=item_data['value'],
                            description=item_data['description']
                        )
                        session.add(item)
                        break
                    except OperationalError as e:
                        if "database is locked" in str(e):
                            retries -= 1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise
                    except IntegrityError:
                        print(f"IntegrityError: Failed to insert dashboard item: {item_data['title']}")
                        session.rollback()

            try:
                session.commit()
                print("All dashboard items committed successfully!")
            except OperationalError as e:
                if "database is locked" in str(e):
                    print("Database is locked, retrying...")
                    time.sleep(0.5)
                    session.rollback()
                    session.commit()
                else:
                    raise
            except Exception as e:
                print(f"Error committing dashboard items: {str(e)}")
                session.rollback()

if __name__ == "__main__":
    load_dashboard_items()
    print("Dashboard items loaded successfully!")
