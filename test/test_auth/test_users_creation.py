import pytest
import requests


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        # print(resp.text)
        assert resp.status_code == 200

    @pytest.mark.parametrize("test_data", [pytest.lazy_fixture("update_user_validations_data")])
    def test_update_user_validations(self, API_URL, sure_user_exists, get_user_by_email, testuser_data,
                                     delete_user_by_email, sure_user_exists_from_test, test_data):
        delete_user_by_email("not_already@existed_email")
        sure_user_exists_from_test(email="existed@email")
        cookies = {}
        logged_in, json, stat_code, passed = test_data
        if logged_in:
            resp = requests.post(API_URL + "/api/v1/accounts/session", json={"email": testuser_data['email'],
                                                                             "password": testuser_data['password']})
            cookies = resp.cookies.get_dict()

        upd_resp = requests.patch(f"{API_URL}/api/v1/accounts", json=json, cookies=cookies)

        # response status
        assert upd_resp.status_code == stat_code

        # check in db
        if 200 == stat_code:
            if passed:
                assert get_user_by_email(json['email']) is not None
            else:
                assert get_user_by_email(json['email']) is None

    def test_login(self, API_URL, sure_user_exists, get_user_by_email, testuser_data):
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

    @pytest.mark.parametrize("test_data", [pytest.lazy_fixture('login_test_data')])
    def test_login_validations(self, API_URL, sure_user_exists, get_user_by_email, test_data):
        json, code, mess = test_data
        resp = requests.post(API_URL + "/api/v1/accounts/session", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()['msg'][0]['msg'] == mess
        # print(resp.headers)
        assert resp.cookies.get_dict() == {}

    @pytest.mark.parametrize("test_data", [pytest.lazy_fixture('registration_data')])
    def test_create_user_validations(self, API_URL, sure_user_not_exists, get_user_by_email, test_data):
        json, code, mess = test_data
        resp = requests.post(API_URL + "/api/v1/accounts", json=json)
        print(resp.text)
        assert resp.status_code == code
        assert resp.json()['msg'][0]['msg'] == mess
        assert get_user_by_email(json['email']) is None

    def test_create_user(self, API_URL, sure_user_not_exists, get_user_by_email, testuser_data):
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