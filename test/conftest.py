import pytest
from app.mod_auth.models import User
from app import db


def tech_testuser_data():
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSziy"}


@pytest.fixture(scope="function")
def testuser_data():
    return tech_testuser_data()


@pytest.fixture(scope="session")
def API_URL():
    return "http://localhost:8080"


def tech_get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def tech_delete_user_by_email(email):
    user = tech_get_user_by_email(email)
    print('*****************/////////////////')
    print(user)
    if user is not None:
        db.session.delete(user)
        db.session.commit()


def tech_insert_user():
    user = User(email=tech_testuser_data()['email'], password=tech_testuser_data()['pass_hash'])
    db.session.add(user)
    db.session.commit()


@pytest.fixture(scope="function")
def is_user_logged_in_by_email():
    def _method():
        tech_get_user_by_email(email)
    return _method


@pytest.fixture(scope="function")
def sure_user_exists():
    def _method(email, password):
        tech_delete_user_by_email(email)
        tech_insert_user()
    return _method


@pytest.fixture(scope="function")
def delete_user_by_email():
    def _method(email):
        # user = tech_get_user_by_email(email)
        # print('*****************/////////////////')
        # print(user)
        # if user is not None:
        #     db.session.delete(user)
        #     db.session.commit()
        tech_delete_user_by_email(email)

    return _method


@pytest.fixture(scope="function")
def get_user_by_email():
    def _method(email):
        return tech_get_user_by_email(email)

    return _method
