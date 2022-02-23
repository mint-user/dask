from sqlalchemy.orm import relationship

from app import db
# from app.auth.models import User


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Task(Base):
    __tablename__ = "tasks"
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = relationship("User", backref="tasks")

    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    # parent = relationship('Task', backref="tasks")


# db.create_all()
