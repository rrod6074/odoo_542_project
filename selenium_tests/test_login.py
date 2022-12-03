import time

from selenium_utils import SeleniumBaseTestCase


class OdooLogin(SeleniumBaseTestCase):
    def test_successful_login(self):
        result = self.selenium_util.login("admin", "admin")
        time.sleep(1)
        self.assertTrue(result)

    def test_logout(self):
        self.selenium_util.login("admin", "admin")
        self.selenium_util.logout()
        result = self.selenium_util.is_login_form_available()
        time.sleep(1)
        self.assertTrue(result)

    def test_failed_login(self):
        result = self.selenium_util.login("admin", "notadmin")
        self.assertFalse(result)

    def test_failed_login_error_prompt(self):
        self.selenium_util.login("admin", "notadmin")
        result = self.selenium_util.get_wrong_login_password_available()
        if result:
            self.assertEqual(result.text, "Wrong login/password")
        else:
            self.assertIsNotNone(result)