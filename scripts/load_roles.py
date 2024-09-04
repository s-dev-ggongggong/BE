# scripts/load_roles.py

from extensions import db
from models.role import Role
from __init__ import create_app

app = create_app()

roles = [
    "인턴", "사원", "주임", "계장", "대리", "과장", "차장", "부장", "감사",
    "이사", "상무", "전무", "부사장", "사장", "임원",
    "연구원", "주임연구원", "선임연구원", "책임연구원", "수석연구원", "연구소장"
]

with app.app_context():
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            db.session.add(role)

    db.session.commit()
    print("Roles have been populated.")
