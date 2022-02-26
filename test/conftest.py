import pytest
import requests


# @pytest.fixture(scope="module")
# def user_is_logged_in(API_URL, testuser_data):
#     def _method():
#         resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": "dimas@js",
#                                                                          "password": "QWE123qwe"})
#         cookies = resp.cookies.get_dict()
#         return cookies
#     return _method


@pytest.fixture(scope="session")
def API_URL():
    return "http://localhost:8080"


@pytest.fixture(scope="package")
def tech_testuser_data():
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$pGO0MWWM9I5GvzLN8PrKSeJtjMN8E8i30t79ghvqUqpWce1jxAqKu",
            "token": "504dc0bf28a30e67a6929126b1e91cc1"}


@pytest.fixture(scope="package")
def testuser_data():
    # return tech_testuser_data()
    return {"email": "qwe@qwe",
            "password": "oIwi5jdPJlLGzba",
            "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSziy",
            "token": "504dc0bf28a30e67a6929126b1e91cc1"}

@pytest.fixture(scope="function")
def user_is_logged_in():
    pass