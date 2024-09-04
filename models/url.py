from extensions import db

class Url(db.Model):
    __tablename__ = 'url'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Url {self.url}>'
