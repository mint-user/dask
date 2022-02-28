import pytest


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def input_field_by_id(self, html_id, text):
        field = self.driver.find_element_by_id(html_id)
        field.send_keys(text)


class AuthPage(BasePage):
    def __init__(self, driver):
        super(AuthPage, self).__init__(driver)

    def open(self):
        self.driver.get('http://localhost:8080')
        self.heading_text_is("Login")
        self.error_message_is("")

    def heading_text_is(self, expected_text):
        heading = self.driver.find_element_by_xpath("//header/h1")
        assert heading.text == expected_text

    def input_email(self, text):
        super(AuthPage, self).input_field_by_id("email", text)

    def input_password(self, text):
        super(AuthPage, self).input_field_by_id("password", text)

    def submit_form(self):
        submit_btn = self.driver.find_element_by_id("submit")
        submit_btn.click()

    def error_message_is(self, message):
        error_block_text = self.driver.find_element_by_id("error").text
        assert error_block_text == message, f"Wrong error message, should be '{message}, got '{error_block_text}'"
