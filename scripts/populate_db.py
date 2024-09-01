import os,sys ,time, bcrypt ,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from run import create_app,db
from models.dashboard import DashboardItem
from models.email import Email
from models.user import User
from sqlalchemy.exc import OperationalError ,IntegrityError
from extensions import session_scope



def populate_database():
    app=create_app()
    with app.app_context():
        with session_scope() as session:
            users_data = [
                {"username": "test1", "email": "test1@example.com", "password": "password1"},
                {"username": "test2", "email": "test2@example.com", "password": "password2"},
                {"username": "test3", "email": "test3@example.com", "password": "password3"},
                {"username": "test4", "email": "test4@example.com", "password": "password4"},
                {"username": "test5", "email": "test5@example.com", "password": "password5"}
            ]
            #with db.session.no_autoflush:
                        
            for user_data in users_data:
                # hashed_password =bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
                # user_data['password_hash'] = hashed_password.decode('utf-8')
                # user_data.pop('password')

    #                if 'password' in user_data:    

                retries=5
                while retries>0:
                    try:
                        if not User.query.filter_by(email=user_data['email']).first():
                            #user = User(**user_data)
                            user = User(
                                username=user_data['username'],
                                email=user_data['email'],
                                password=user_data['password']
                            )

                            session.add(user)
                            session.commit()

                            print(f"Added user: {user_data['email']}")
                        else:
                            print(f"{user_data['email']} exists!")
                        break
                    except IntegrityError :
                        print(f"IntegrityError {user_data['email']} exist!")
                        session.rollback()
                    
                    except OperationalError as e :
                        if "database is locked" in str(e):
                            retries -=1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise
            # Insert Dashboard Items

            dashboard_items = [
                {"title": "Total Users", "value": "1000", "description": "Numr of registered users"},
                {"title": "Active Users", "value": "750", "description": "Users active in the last 30 days"}
            ]

            for item_data in dashboard_items:
                retries =5
                while retries>0:
                    try:    
                        item = DashboardItem(**item_data)
                        session.add(item)
                        break
                    except OperationalError as e:
                        if "database is locked" in str(e):
                            retries -=1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise

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
                retries =5
                while retries>0:
                    try:
                        email_obj = Email(**email)    
                        session.add(email_obj)
                        break
                    except OperationalError as e:
                        if "database is locked" in str(e):
                            retries -=1
                            time.sleep(0.5)
                            session.rollback()
                        else:
                            raise
            
                session.add(email_obj)

            try:
                session.commit()
                print("All data committed successfully!")
            except OperationalError as e:
                if "database is locked" in str(e):
                    print("Database is locked, retrying...")
                    time.sleep(0.5)
                    session.rollback()
                    session.commit()
                else:
                    raise
            except Exception as e:
                print(f"Error committing data: {str(e)}")
                db.session.rollback()

if __name__ == "__main__":
    populate_database()
    print("Database populated successfully!")