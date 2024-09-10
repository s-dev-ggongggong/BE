from functools  import wraps
from flask import jsonify
from extensions import db

def m_handle_exception(f):
    @wraps(f)
    def decorated_function(*args,**kwagrs):
        try:
            return f(*args,**kwagrs)
        except Exception as e:
            db.session.rollback()
            print(f'Arror ocrrued :{str(e)}')
            raise
    return decorated_function


