from extensions import db
from sqlalchemy.exc import IntegrityError

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError:
            db.session.rollback()
            return None

