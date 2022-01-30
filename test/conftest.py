import pytest
from app.mod_auth.models import User
from app import db


@pytest.fixture(scope="session")
def API_URL():
    return "http://localhost:8080"


@pytest.fixture(scope="function")
def delete_user_by_email():
    def _method(email):
        user = User.query.filter(User.email == email).first()
        print('*****************/////////////////')
        print(user)
        if not user is None:
            db.session.delete(user)
            db.session.commit()
            # user.delete()
            # return str(user)

    return _method
