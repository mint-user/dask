# from flask_sqlalchemy import SQLAlchemy
from main import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String)
    token_expires = db.Column(db.DateTime)

    def __repr__(self):
        return "<User %r>" % self.email