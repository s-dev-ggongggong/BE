import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from app import create_app
from extensions import db
from models.role import Role
from scripts.utils import load_json
def load_roles(file_path):
    app = create_app()
    with app.app_context():
        data = load_json(file_path)
        for item in data:
            existing = Role.query.filter_by(name=item['name']).first()
            if not existing:
                role = Role(**item)
                db.session.add(role)
        db.session.commit()

if __name__ == '__main__':
    load_roles('data/roles.json')