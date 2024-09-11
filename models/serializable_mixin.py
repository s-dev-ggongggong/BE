# models/serializable_mixin.py
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import date, datetime

class SerializableMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        def converter(o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
            if isinstance(o, DeclarativeMeta):
                return o.to_dict()
        return json.dumps(self.to_dict(), default=converter)
