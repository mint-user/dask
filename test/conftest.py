import pytest
import requests
from app import db
from app.auth.models import User
from app.tasks.models import Task


@pytest.fixture(scope="session")
def API_URL(request):
    return "http://localhost:8080"


def _testuser_data():
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSziy",
            "token": "504dc0bf28a30e67a6929126b1e91cc1"}


@pytest.fixture(scope="package")
def testuser_data():
    return _testuser_data()


@pytest.fixture(scope="class")
def sure_user_exists(insert_user, delete_user_by_email, testuser_data):
    user = User.query.filter(User.email == testuser_data['email']).first()
    if user is None:
        user = insert_user(testuser_data['email'], testuser_data['pass_hash'])
    else:
        if user.password != testuser_data['pass_hash']:
            user.password = testuser_data['pass_hash']
            db.session.add(user)
            db.session.commit()
    # delete_user_by_email(testuser_data['email'])
    yield user


@pytest.fixture(scope="class")
def user_with_no_tasks_loggen_in(sure_user_exists, API_URL, testuser_data, request):
    user = sure_user_exists
    user_tasks = Task.query.filter(Task.user_id == user.id).all()
    for user_task in user_tasks:
        db.session.delete(user_task)
    db.session.commit()
    resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                     "password": testuser_data['password']})
    cookies = resp.cookies.get_dict()
    assert "access_token_cookie" in cookies.keys()
    # return cookies
    request.cls.cookies = cookies
    yield


@pytest.fixture(scope="function")
def logged_in_cookies(API_URL, sure_user_exists, testuser_data):
    resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                     "password": testuser_data['password']})
    cookies = resp.cookies.get_dict()
    assert "access_token_cookie" in cookies.keys()
    yield cookies


@pytest.fixture(scope="class")
def get_user_by_email():
    def _method(email):
        return User.query.filter(User.email == email).first()
    return _method


@pytest.fixture(scope="class")
def delete_user_by_email(get_user_by_email, testuser_data):
    def _method(email):
        user = get_user_by_email(email)
        if user is not None:
            user_tasks = Task.query.filter(Task.user_id == user.id).all()
            for user_task in user_tasks:
                db.session.delete(user_task)

            db.session.delete(user)
            db.session.commit()
    return _method


@pytest.fixture(scope="class")
def insert_user():
    def _method(email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    return _method