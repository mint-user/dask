import pytest
from test.conftest import _testuser_data


@pytest.fixture()
def my_params():
    return [
        (False, {"email": _testuser_data()['email'], "password": _testuser_data()['password']}, 401, False),
        (True, {"email": "not_already@existed_email", "password": _testuser_data()['password']}, 200, True),
        (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87Hdfgfdgdfgdfgdfgdfg"}, 400, True),
        (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87H"}, 200, True),
        (True, {"email": "existed@email", "password": _testuser_data()['password']}, 400, False)
    ]


@pytest.fixture(params=[
    (False, {"email": _testuser_data()['email'], "password": _testuser_data()['password']}, 401, False),
    (True, {"email": "not_already@existed_email", "password": _testuser_data()['password']}, 200, True),
    (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87Hdfgfdgdfgdfgdfgdfg"}, 400, True),
    (True, {"email": "not_already@existed_email", "password": "abraQWE123u80n)87H"}, 200, True),
    (True, {"email": "existed@email", "password": _testuser_data()['password']}, 400, False)
])
def update_user_validations_data(request):
    return request.param


@pytest.fixture(params=[
    ({"email": _testuser_data()['email']}, 400, "field required"),
    ({"email": "email", "password": "pqwe123QWDsdf"}, 400, "Email must contain '@'"),
    ({"email": _testuser_data()['email'], "password": "pqe1F"}, 400, "Password should contain 8..20 characters"),
    (
    {"email": _testuser_data()['email'], "password": "pqe1Fsssssssssssssssssssssssssssssssssssssssssssssssss"}, 400,
    "Password should contain 8..20 characters"),
    ({"email": _testuser_data()['email'], "password": "DSDSGSDF988593285"}, 400,
     "Password should contain lowercase letters"),
    ({"email": _testuser_data()['email']}, 400, "field required")
])
def registration_data(request):
    return request.param


@pytest.fixture(scope="function")
def sure_user_exists_from_test(insert_user, delete_user_by_email, testuser_data):
    def _method(email, pass_hash=testuser_data['pass_hash']):
        delete_user_by_email(email)
        insert_user(email, pass_hash)
    return _method


@pytest.fixture(scope="function")
def sure_user_not_exists(delete_user_by_email, testuser_data):
    delete_user_by_email(testuser_data['email'])
    yield
    delete_user_by_email(testuser_data['email'])


@pytest.fixture(params=[
    ({"email": "qwewasd@qwe1111", "password": "1"}, 400, "Wrong email or password"),
    ({"email": _testuser_data()['email'], "password": "111"}, 400, "Wrong email or password"),
    ({}, 400, "field required")
])
def login_test_data(request):
    return request.param
