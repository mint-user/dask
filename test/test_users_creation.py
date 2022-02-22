from datetime import datetime

import pytest
import requests
# from pytest_lazyfixture


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200

    testuser_data = {"email": "qwe@qwe",
                     "password": "oIwi5jdPJlLGzba",
                     "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSzi",
                     "token": "504dc0bf28a30e67a6929126b1e91cc1"}

    def test_login(self, API_URL, sure_user_exists, get_user_by_email, testuser_data):
        sure_user_exists(testuser_data['email'], testuser_data['pass_hash'])
        resp = requests.post(API_URL + "/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                         "password": testuser_data['password']})
        # check response structure
        print(resp.text)
        assert resp.status_code == 200

        cookies = resp.cookies.get_dict()

        assert "access_token_cookie" in cookies
        assert "refresh_token_cookie" in cookies

        # LOGOUT
        resp = requests.delete(API_URL + "/api/v1/accounts/session",
                               cookies={"access_token_cookie": cookies["access_token_cookie"],
                                        "refresh_token_cookie": cookies["refresh_token_cookie"]})

        assert resp.cookies.items() == []

    login_data = [
        ({"email": "qwewasd@qwe1111", "password": "1"}, 401, "Wrong email or password"),
        ({"email": testuser_data['email'], "password": "111"}, 401, "Wrong email or password"),
        ({}, 400, "Bad request")
    ]

    @pytest.mark.parametrize("json, code, mess", login_data)
    def test_login_validations(self, API_URL, sure_user_exists, get_user_by_email, testuser_data, json, code, mess):
        sure_user_exists(testuser_data['email'], testuser_data['pass_hash'])
        resp = requests.post(API_URL + "/api/v1/accounts/session", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()["error"] == mess
        user = get_user_by_email(testuser_data['email'])
        # print(resp.headers)
        assert resp.cookies.get_dict() == {}
        # print("user: {}", user)

    @pytest.mark.parametrize("test_data", [pytest.lazy_fixture('registration_data')])
    def test_create_user_validations(self, API_URL, delete_user_by_email, get_user_by_email, test_data):
        json, code, mess = test_data
        delete_user_by_email(json['email'])
        resp = requests.post(API_URL + "/api/v1/accounts", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()['msg'][0]['msg'] == mess
        assert get_user_by_email(json['email']) is None

    def test_create_user(self, API_URL, delete_user_by_email, get_user_by_email, testuser_data):
        # setup
        delete_user_by_email(testuser_data['email'])

        # create user
        resp = requests.post(API_URL + "/api/v1/accounts",
                             json={"email": testuser_data['email'], "password": "pqwe123QWDsdf"})
        print("RESPONSE 'create uer'", resp.text)
        assert resp.status_code == 201

        # check user in DB
        user = get_user_by_email(testuser_data['email'])
        assert user is not None
        assert user.email == testuser_data['email']

        # create user with existed email
        resp = requests.post(API_URL + "/api/v1/accounts",
                             json={"email": testuser_data['email'], "password": "pqwe123QWDsdf"})
        print("RESPONSE 'create user with existed email'", resp.text)
        assert resp.status_code == 400
        user = get_user_by_email(testuser_data['email'])
        assert user is not None
        assert user.email == testuser_data['email']
        assert resp.json()['msg'][0]['msg'] == "Email is already used"
