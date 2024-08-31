import json
from app import create_app,db
from models.models import User, DashboardItem, Email, Training
from datetime import datetime

def populate_database():
    app=create_app()
    with app.app_context():
        users_data = [
            {"username": "test1", "email": "test1@example.com", "password_hash": "hashed_password"},
            {"username": "test2", "email": "test2@example.com", "password_hash": "hashed_password"},
            {"username": "test3", "email": "test3@example.com", "password_hash": "hashed_password"},
            {"username": "test4", "email": "test4@example.com", "password_hash": "hashed_password"},
            {"username": "test5", "email": "test5@example.com", "password_hash": "hashed_password"}
        ]
        for user_data in users_data:
            if not User.query.filter_by(email=user_data['email']).first():
                user = User(**user_data)
                db.session.add(user)
            else:
                print(f"Users with email {user_data['email']} already exists")

        # Insert Dashboard Items
        dashboard_items = [
            {"title": "Total Users", "value": "1000", "description": "Number of registered users"},
            {"title": "Active Users", "value": "750", "description": "Users active in the last 30 days"}
        ]
        for item_data in dashboard_items:
            item = DashboardItem(**item_data)
            db.session.add(item)

        # Insert Email Data
        email_data = [
            {
                "subject": "Welcome to our company",
                "body": "Thank you for signing up!",
                "sender": "support@example.com",
                "recipient": "test1@example.com",
                "sent_date": datetime.utcnow()
            },
            {
                "subject": "Your weekly report",
                "body": "Here's your activity summary for the week.",
                "sender": "reports@example.com",
                "recipient": "test2@example.com",
                "sent_date": datetime.utcnow()
            },
            {
                "subject": "[AD] Suggestion for developer Tools",
                "body": "Tools for developer.",
                "sender": "unkown@example.com",
                "recipient": "test3@example.com",
                "sent_date": datetime.utcnow()
            },
              {
                "subject": "Your HR Score reports",
                "body": "Here's your Test Score.",
                "sender": "HR@example.com",
                "recipient": "test4@example.com",
                "sent_date": datetime.utcnow()
            },
            {
                "subject": "IT-DEV team assignment",
                "body": "This is daily mission for junior.",
                "sender": "IT.dep@example.com",
                "recipient": "test5@example.com",
                "sent_date": datetime.utcnow()
            },
        ]  

            
        for email in email_data:
            email_obj = Email(**email)
            db.session.add(email_obj)

        # Commit all changes
        db.session.commit()

if __name__ == "__main__":
    populate_database()
    print("Database populated successfully!")