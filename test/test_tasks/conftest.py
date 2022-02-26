import pytest
import requests

from app import db
from app.auth.models import User


@pytest.fixture(scope="function")
def user_is_logged_in(API_URL, insert_user, delete_user_by_email, testuser_data):
# def user_is_logged_in(API_URL, delete_user_by_email, testuser_data):
    def _method():
        delete_user_by_email(testuser_data['email'])
        insert_user(testuser_data['email'], testuser_data['pass_hash'])
        resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                         "password": testuser_data['password']})
        cookies = resp.cookies.get_dict()
        assert cookies != {}
        return cookies
    return _method


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
