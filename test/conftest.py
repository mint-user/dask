import pytest
from app.mod_auth.models import User
from app import db


@pytest.fixture(scope="function")
def testuser_email():
    return "qwe@qwe"


@pytest.fixture(scope="session")
def API_URL():
    return "http://localhost:8080"


def get_user_ny_email(email):
    return User.query.filter(User.email == email).first()


@pytest.fixture(scope="function")
def delete_user_by_email():
    def _method(email):
        user = get_user_ny_email(email)
        print('*****************/////////////////')
        print(user)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

    return _method


@pytest.fixture(scope="function")
def user_exists_by_email():
    def _method(email):
        return get_user_ny_email(email)

    return _method
