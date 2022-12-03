import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class SeleniumBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.selenium_util = SeleniumUtil()

    def tearDown(self):
        time.sleep(1)
        self.selenium_util.quit()


class SeleniumUtil:
    def __init__(self):
        """
        Selenium utility for controlling Chrome browser state.
        """
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def quit(self):
        """
        Closes the WebDriver.
        :return: None
        """
        self.driver.quit()

    def get_url(self, url):
        """
        Navigate WebDriver to the target URL.
        :param url: link to webpage
        :return: the result of navigating to the url as returned by selenium
        """
        return self.driver.get(url)

    def get_element(self, by, value):
        """
        Returns the element on the page
        :param by: search By type
        :param value: search value
        :return: the target element if found, else returns None
        """
        return self.driver.find_element(by, value)

    def is_element_present(self, by, value):
        """
        Checks if an element is present without exceptions
        :param by: search type
        :param value: search value
        :return: True if found, False if not found
        """

        """
        self.get_element(by, value)
        return True
        """

        try:
            self.get_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def update_form_field_by_element_name(self, field_name, field_value):
        """
        Updates the form fields based on name
        :param field_name: HTML field name to find
        :param field_value: input value
        :return: None
        """
        search_bar = self.get_element(By.NAME, field_name)
        search_bar.clear()
        time.sleep(1)
        search_bar.send_keys(field_value)

    def login(self, username, password):
        """
        Navigate to login page and submit user credentials
        :param username: login name
        :param password: login password
        :return: True if logout button exists, False if it does not
        """
        self.get_url("http://odoo-server:8069/web/login")
        if self.is_login_form_available():
            self.update_form_field_by_element_name("login", username)
            self.update_form_field_by_element_name("password", password)
            self.get_element(By.NAME, "login").send_keys(Keys.RETURN)
            time.sleep(1)
            return self.is_element_present(By.CLASS_NAME, "o_navbar_apps_menu")
        else:
            return False

    def _show_user_menu(self):
        """
        Internal method to show the user menu.
        :return: None
        """
        user_menu_class = "o_user_menu"
        menu_button = self.get_element(By.CLASS_NAME, user_menu_class)
        menu_button.click()
        time.sleep(1)

    def _show_logout_button(self):
        """
        Internal method to show the logout button.
        :return: None
        """
        self._show_user_menu()
        expanded_menu = self.get_element(By.CLASS_NAME, "o-dropdown--menu")
        expanded_menu.click()
        time.sleep(1)

    def is_logout_button_available(self):
        """
        Checks if the logout button is found on the page
        :return: True if button exists, False if it does not exist
        """
        return self.is_element_present(By.LINK_TEXT, "Log out")

    def logout(self):
        """
        Log out of the user account
        :return: True if successful, False if unsuccessful
        """
        self._show_logout_button()
        if self.is_logout_button_available():
            button = self.get_element(By.LINK_TEXT, "Log out")
            button.click()
            return True
        else:
            return False

    def is_login_form_available(self):
        """
        Checks if the login form is found on the page
        :return: True if button exists, False if it does not
        """
        return self.is_element_present(By.NAME, "login")

    def get_wrong_login_password_available(self):
        if self.is_element_present(By.CLASS_NAME, "alert"):
            return self.get_element(By.CLASS_NAME, "alert")
        else:
            return None
