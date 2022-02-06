import pytest
import requests


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        # resp = requests.get("http://127.0.0.1:5000")
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200

    testuser_email = "qwe@qwe"

    date = [
        ({"email": testuser_email}, 400, "Request should contain 'email' and 'password' fields"),
        ({"email": "email", "password": "pqwe123QWDsdf"}, 400, "Email should contain '@'"),
        ({"email": testuser_email, "password": "pqe1F"}, 400, "Password should contain 8..20 characters"),
        ({"email": testuser_email, "password": "pqe1Fsssssssssssssssssssssssssssssssssssssssssssssssss"}, 400,
         "Password should contain 8..20 characters"),
        ({"email": testuser_email, "password": "DSDSGSDF988593285"}, 400, "Password should contain lowercase letters"),
        ({"email": testuser_email}, 400, "Request should contain 'email' and 'password' fields")
    ]

    @pytest.mark.parametrize("json, code, mess", date)
    def test_create_user_validations(self, API_URL, delete_user_by_email, user_exists_by_email, json, code, mess):
        delete_user_by_email(json['email'])
        resp = requests.post(API_URL + "/api/v1/accounts", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()["error"] == mess
        assert user_exists_by_email(json['email']) is None

    def test_create_user(self, API_URL, delete_user_by_email, user_exists_by_email, testuser_email):
        # email = "qwe@qwe"
        delete_user_by_email(testuser_email)

        resp = requests.post(API_URL + "/api/v1/accounts", json={"email": testuser_email, "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 201
        user = user_exists_by_email(testuser_email)
        assert user is not None
        assert user.email == testuser_email

        resp = requests.post(API_URL + "/api/v1/accounts", json={"email": testuser_email, "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 202
        user = user_exists_by_email(testuser_email)
        assert user is not None
        assert user.email == testuser_email
        assert resp.json()["error"] == "Email is already used"
