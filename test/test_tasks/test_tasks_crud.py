import json
from time import sleep

import pytest
import requests
from faker import Faker
from faker.providers import lorem
from selenium.webdriver.support import expected_conditions as EC

fake = Faker()
fake.add_provider(lorem)


class TestNotLoggedInTasksValidationsCRUD:

    # def test_server_is_up(self, API_URL):
    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        assert resp.status_code == 200

    @pytest.mark.parametrize("resp_type, data", [
        # ("post", {"name": "newC task", "parent_task_id": 1}),
        ("post", {"name": fake.sentence(), "parent_task_id": 1}),
        ("get", {"name": fake.sentence(), "parent_task_id": 1}),
        ("delete", {"name": fake.sentence(), "parent_task_id": 1}),
    ])
    def test_forbid_tasks_crud_for_not_authenticated(self, API_URL, resp_type, data):
        req = getattr(requests, resp_type)
        if resp_type == "delete":
            resp = req(f"{API_URL}/api/v1/tasks")
        else:
            resp = req(f"{API_URL}/api/v1/tasks", data)

        assert resp.json()["msg"] == 'Missing cookie "access_token_cookie"'


@pytest.mark.usefixtures("user_with_no_tasks_loggen_in")
class TestLoggedInTasksValidationsCRUD:

    @pytest.mark.parametrize("data", [pytest.lazy_fixture("task_creation_validation_data")])
    def test_creation_tasks_validation(self, API_URL, data):
        logged_in_cookies = self.cookies
        data, code, message = data
        resp = requests.post(f"{API_URL}/api/v1/tasks", json.dumps(data),
                             cookies=logged_in_cookies)

        msg = resp.json()["msg"] if code == 201 else resp.json()["msg"][0]["msg"]
        assert msg == message


@pytest.mark.usefixtures("selenium")
class TestWeb:

    def test_login_page_is_visible(self):
        self.driver.get('http://localhost:8080')
        heading = self.driver.find_element_by_xpath("//header/h1")
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("password")
        submit_btn = self.driver.find_element_by_id("submit")
        error_block = self.driver.find_element_by_id("error")

        assert error_block.text == ""
        assert heading.text == "Login"
        EC.presence_of_element_located(email_field)
        # fill fields
        email_field.send_keys("ert")
        password_field.send_keys("ert")
        submit_btn.click()
        sleep(1)

        #check error
        error_block.text == "Wrong email or password"
