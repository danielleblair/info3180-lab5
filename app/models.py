
# Add any model classes for Flask-SQLAlchemy here

from . import db
from werkzeug.security import generate_password_hash

from sqlalchemy.sql import func


class Movie(db.Model):
    
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    poster = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, title, description, poster):
        self.title = title
        self.description = description
        self.poster = poster
        self.created_at = func.now()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)