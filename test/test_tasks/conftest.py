import pytest

from app import db
from app.auth.models import User


@pytest.fixture()
def tech_get_user_by_email():
    def _method(email):
        return User.query.filter(User.email == email).first()
    return _method


@pytest.fixture()
def delete_user_by_email(tech_get_user_by_email, testuser_data):
    def _method(email):
        user = tech_get_user_by_email(email)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
    return _method


@pytest.fixture()
def insert_user():
    def _method(email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    return _method
