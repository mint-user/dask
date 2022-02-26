import pytest
from app.auth.models import User
from app import db


def tech_testuser_data():
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSziy",
            "token": "504dc0bf28a30e67a6929126b1e91cc1"}


@pytest.fixture(params=[
    (False, {"email": tech_testuser_data()['email'], "password": tech_testuser_data()['password']}, 401, False),
    (True, {"email": "not_already@existed_email", "password": tech_testuser_data()['password']}, 200, True),
    (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87Hdfgfdgdfgdfgdfgdfg"}, 400, True),
    (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87H"}, 200, True),
    (True, {"email": "existed@email", "password": tech_testuser_data()['password']}, 400, False)
])
def update_user_validations_data(request):
    return request.param


@pytest.fixture(params=[
        ({"email": tech_testuser_data()['email']}, 400, "field required"),
        ({"email": "email", "password": "pqwe123QWDsdf"}, 400, "Email must contain '@'"),
        ({"email": tech_testuser_data()['email'], "password": "pqe1F"}, 400, "Password should contain 8..20 characters"),
        ({"email": tech_testuser_data()['email'], "password": "pqe1Fsssssssssssssssssssssssssssssssssssssssssssssssss"}, 400,
         "Password should contain 8..20 characters"),
        ({"email": tech_testuser_data()['email'], "password": "DSDSGSDF988593285"}, 400,
         "Password should contain lowercase letters"),
        ({"email": tech_testuser_data()['email']}, 400, "field required")
    ])
def registration_data(request):
    return request.param


@pytest.fixture(scope="function")
def testuser_data():
    return tech_testuser_data()


def tech_get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def _insert_user(email=tech_testuser_data()['email'],
                     password=tech_testuser_data()['pass_hash']):
    user = User(email=email,
                password=password)
    db.session.add(user)
    db.session.commit()


@pytest.fixture(scope="function")
def sure_user_exists_from_test():
    def _method(email=tech_testuser_data()['email'], password=tech_testuser_data()['pass_hash']):
        _delete_user_by_email(email)
        _insert_user(email, password)
    return _method


@pytest.fixture(scope="function")
def sure_user_exists(email=tech_testuser_data()['email'], password=tech_testuser_data()['pass_hash']):
    _delete_user_by_email(email)
    _insert_user(email, password)
    yield


def _delete_user_by_email(email=tech_testuser_data()['email']):
    user = tech_get_user_by_email(email)
    if user is not None:
        db.session.delete(user)
        db.session.commit()


@pytest.fixture(scope="function")
def delete_user_by_email():
    def _method(email):
        _delete_user_by_email(email)
    return _method


@pytest.fixture(scope="function")
def sure_user_not_exists(email=tech_testuser_data()['email']):
    _delete_user_by_email(email)
    yield
    _delete_user_by_email(email)


@pytest.fixture(scope="function")
def get_user_by_email():
    def _method(email):
        return tech_get_user_by_email(email)
    return _method


@pytest.fixture(params=[
        ({"email": "qwewasd@qwe1111", "password": "1"}, 400, "Wrong email or password"),
        ({"email": tech_testuser_data()['email'], "password": "111"}, 400, "Wrong email or password"),
        ({}, 400, "field required")
    ])
def login_test_data(request):
    return request.param
