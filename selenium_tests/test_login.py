import time

from selenium_utils import SeleniumBaseTestCase


class OdooLoginInteraction(SeleniumBaseTestCase):
    def test_successful_login(self):
        """
        positive test case:
        tests simple account login
        checks for user menu upon successful login
        """
        result = self.odoo_selenium_util.login("admin", "admin")
        time.sleep(1)
        self.assertTrue(result)

    def test_logout(self):
        """
        positive test case:
        tests simple account logout
        checks for user login form after logging out
        """
        self.odoo_selenium_util.login("admin", "admin")
        self.odoo_selenium_util.show_logout_button()
        self.odoo_selenium_util.logout()
        result = self.odoo_selenium_util.is_login_form_available()
        time.sleep(1)
        self.assertTrue(result)

    def test_failed_login(self):
        """
        negative test case:
        tests for login with invalid credentials
        checks that user is still on the odoo homepage after providing invalid credentials
        """
        result = self.odoo_selenium_util.login("admin", "notadmin")
        self.assertFalse(result)

    def test_failed_login_error_prompt(self):
        """
        negative test case:
        tests for login with invalid credentials
        checks that user is presented with an error message
        """
        self.odoo_selenium_util.login("admin", "notadmin")
        result = self.odoo_selenium_util.get_wrong_login_password_available()
        if result:
            self.assertEqual(result.text, "Wrong login/password")
        else:
            self.assertIsNotNone(result)
