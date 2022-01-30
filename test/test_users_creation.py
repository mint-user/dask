import requests
import string


# def delete_user_by_email(email):
#     pass


class TestUserCreation:

    def test_server_is_up(self, API_URL):
        # resp = requests.get("http://127.0.0.1:5000")
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200

    def test_create_user(self, API_URL, delete_user_by_email):
        email = "qwe@qwe"
        delete_user_by_email(email)
        resp = requests.post(API_URL, {"email": email, "password": "pqwe123QWDsdf"})
        print(resp.text)
        assert resp.status_code == 201
