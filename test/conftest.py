import pytest
import requests


@pytest.fixture(scope="session")
def API_URL():
    return "http://localhost:8080"


@pytest.fixture(scope="package")
def testuser_data():
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSziy",
            "token": "504dc0bf28a30e67a6929126b1e91cc1"}


@pytest.fixture(scope="function")
def logged_in_cookies(API_URL, insert_user, delete_user_by_email, testuser_data):
    delete_user_by_email(testuser_data['email'])
    insert_user(testuser_data['email'], testuser_data['pass_hash'])
    resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                     "password": testuser_data['password']})
    cookies = resp.cookies.get_dict()
    assert "access_token_cookie" in cookies.keys()
    return cookies
