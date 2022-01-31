import requests


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        # resp = requests.get("http://127.0.0.1:5000")
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200

    def test_create_user(self, API_URL, delete_user_by_email, user_exists_by_email):
        email = "qwe@qwe"
        delete_user_by_email(email)
        resp = requests.post(API_URL+"/api/v1/accounts", json={"email": email, "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 201
        user = user_exists_by_email(email)
        assert user is not None
        assert user.email == email
