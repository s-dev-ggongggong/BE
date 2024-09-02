import os,sys ,time, bcrypt ,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from run import create_app,db
from models.user import User
from sqlalchemy.exc import OperationalError ,IntegrityError
from extensions import session_scope


def load_json(file_path):
    with open(file_path,'r') as file:
        return json.load(file)
    
def load_users():
    app=create_app()
    with app.app_context():
        with session_scope() as session:
            users_data = load_json('static/users.json') 
            #with db.session.no_autoflush:
                        
            for user_data in users_data:
                # user_data.pop('password')
                # user_data['passwordHash'] = hashed_password.decode('utf-8')

    #                if 'password' in user_data:    

                retries=5
                while retries>0:
                    try:
                        if not User.query.filter_by(email=user_data['email']).first():
                        
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
if __name__ == "__main__":
    load_users()
    print("Database populated successfully!")