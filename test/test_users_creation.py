from datetime import datetime

import pytest
import requests


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200

    testuser_data = {"email": "qwe@qwe",
                     "password": "oIwi5jdPJlLGzba",
                     "pass_hash": "$2b$12$VVaaR32gGCpWeCrFIVYuMuoVs/ypwfXRpZrrvXhJj3TQvDsbuSzi",
                     "token": "504dc0bf28a30e67a6929126b1e91cc1"}

    # logout_data = [
    #     ({}, 400, {"error": "Bad request"}, False),
    #     ({"user_id": 1, "token": "8dfafac23e0e"}, 404, {"error": "Wrong user ID or token"}, False),
    #     ({"user_id": 45, "token": testuser_data['token']}, 404, {"error": "Wrong user ID or token"}, False),
    #     ({"user_id": 1, "token": testuser_data['token']}, 200, {}, True)
    # ]
    #
    # @pytest.mark.parametrize("json, code, answer, logouted", logout_data)
    # def test_logout(self, API_URL, sure_user_exists, get_user_by_email, testuser_data, json, code, answer, logouted):
    #     sure_user_exists(testuser_data['email'], testuser_data['pass_hash'], testuser_data['token'])
    #     resp = requests.delete(API_URL + "/api/v1/accounts/session", json=json)
    #     # check response structure
    #     print(resp.text)
    #     assert resp.status_code == code
    #     assert resp.json() == answer
    #     user = get_user_by_email(testuser_data['email'])
    #     print("user: {}", user)
    #     if logouted:
    #         assert user.token is None
    #     else:
    #         assert user.token == testuser_data['token']

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

    registration_data = [
        ({"email": testuser_data['email']}, 400, "Request should contain 'email' and 'password' fields"),
        ({"email": "email", "password": "pqwe123QWDsdf"}, 400, "Email should contain '@'"),
        ({"email": testuser_data['email'], "password": "pqe1F"}, 400, "Password should contain 8..20 characters"),
        ({"email": testuser_data['email'], "password": "pqe1Fsssssssssssssssssssssssssssssssssssssssssssssssss"}, 400,
         "Password should contain 8..20 characters"),
        ({"email": testuser_data['email'], "password": "DSDSGSDF988593285"}, 400,
         "Password should contain lowercase letters"),
        ({"email": testuser_data['email']}, 400, "Request should contain 'email' and 'password' fields")
    ]

    @pytest.mark.parametrize("json, code, mess", registration_data)
    def test_create_user_validations(self, API_URL, delete_user_by_email, get_user_by_email, json, code, mess):
        delete_user_by_email(json['email'])
        resp = requests.post(API_URL + "/api/v1/accounts", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()["error"] == mess
        assert get_user_by_email(json['email']) is None

    def test_create_user(self, API_URL, delete_user_by_email, get_user_by_email, testuser_data):
        # email = "qwe@qwe"
        delete_user_by_email(testuser_data['email'])

        resp = requests.post(API_URL + "/api/v1/accounts",
                             json={"email": testuser_data['email'], "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 201
        user = get_user_by_email(testuser_data['email'])
        assert user is not None
        assert user.email == testuser_data['email']

        resp = requests.post(API_URL + "/api/v1/accounts",
                             json={"email": testuser_data['email'], "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 202
        user = get_user_by_email(testuser_data['email'])
        assert user is not None
        assert user.email == testuser_data['email']
        assert resp.json()["error"] == "Email is already used"
