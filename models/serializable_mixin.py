from datetime import date, datetime
import json

class SerializableMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        def converter(o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
        return json.dumps(self.to_dict(), default=converter)
    
    