from sqlalchemy.orm import relationship

from app import db
from app.tasks.models import Task


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = "users"
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = relationship("Task", backref="user")

    def __repr__(self):
        return "<User %r>" % self.email


# db.create_all()
