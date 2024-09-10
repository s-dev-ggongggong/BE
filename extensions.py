from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from contextlib import contextmanager


db = SQLAlchemy()
ma = Marshmallow()
migrate =Migrate()

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

 