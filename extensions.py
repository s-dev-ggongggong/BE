from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from contextlib import contextmanager
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
migrate =Migrate()
jwt = JWTManager()

@contextmanager
def session_scope():
    session=db.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

 