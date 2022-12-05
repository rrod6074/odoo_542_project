import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class SeleniumBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.odoo_selenium_util = OdooSeleniumUtil()

    def tearDown(self):
        self.odoo_selenium_util.quit()


class OdooSeleniumUtil:
    # id mapping discovered while navigating om_hospital
    patient_id_mapping = {
        "patients": {
            "action_id": 381,
            "text": "Patients"
        },
        "kids": {
            "action_id": 386,
            "text": "Kids"
        },
        "male patients": {
            "action_id": 387,
            "text": "Male Patients"
        },
        "female patients": {
            "action_id": 388,
            "text": "Female Patients"
        },
    }

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

    def navigate_to_url(self, url):
        """
        Navigate WebDriver to the target URL.
        :param url: link to webpage
        :return: the result of navigating to the url as returned by selenium
        """
        return self.driver.get(url)

    def find_element(self, by, value):
        """
        Returns the element on the page
        :param by: search By type
        :param value: search value
        :return: the target element if found, else Selenium Exception is raised
        """
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        """
        Returns the element on the page
        :param by: search By type
        :param value: search value
        :return: list of target elements if found, else Selenium Exception is raised
        """
        return self.driver.find_elements(by, value)

    def is_element_present(self, by, value):
        """
        Checks if an element is present without exceptions
        :param by: search type
        :param value: search value
        :return: True if found, False if not found
        """
        try:
            self.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def update_form_field(self, by, field_name, field_value):
        """
        Find the input box based on element type and identifier and update by value
        :param by: element search type
        :param field_name: name of the element
        :param field_value: value used for input
        :return: None
        """
        input_box = self.find_element(by, field_name)
        input_box.clear()
        input_box.send_keys(field_value)
        time.sleep(1)

    def update_form_field_with_element(self, element, field_value):
        """
        Update element with the value
        :param element: element discovered from webdriver
        :param field_value: input value
        :return: None
        """
        element.send_keys(field_value)
        time.sleep(1)

    def update_form_field_by_element_name(self, field_name, field_value):
        """
        Updates the form fields based on name
        :param field_name: HTML field name to find
        :param field_value: input value
        :return: None
        """
        self.update_form_field(By.NAME, field_name, field_value)

    def update_form_field_by_id(self, field_name, field_value):
        """
        Update the form if searching for the element by id name
        :param field_name: id name
        :param field_value: input value
        :return: None
        """
        self.update_form_field(By.ID, field_name, field_value)

    def update_form_field_by_xpath(self, field_name, field_value):
        """
        Update the form if searching for the element by xpath
        :param field_name: xpath
        :param field_value: input value
        :return: None
        """
        self.update_form_field(By.XPATH, field_name, field_value)

    def update_dropdown_menu_choice(self, by, field_name, field_value):
        """
        Make a selection in a dropdown menu
        :param by: search type for element
        :param field_name: keyword for locating the element
        :param field_value: input value
        :return: None
        """
        dropdown_menu = Select(self.find_element(by, field_name))
        dropdown_menu.select_by_value(field_value)

    def login(self, username, password):
        """
        Navigate to login page and submit user credentials
        :param username: login name
        :param password: login password
        :return: True if logout button exists, False if it does not
        """
        self.navigate_to_url("http://odoo-server:8069/web/login")
        if self.is_login_form_available():
            self.update_form_field_by_element_name("login", username)
            self.update_form_field_by_element_name("password", password)
            self.driver.save_screenshot(f"login_{username}_{password}_input_credentials.png")
            self.find_element(By.NAME, "login").send_keys(Keys.RETURN)
            time.sleep(1)
            self.driver.save_screenshot(f"login_{username}_{password}_login_result.png")
            return self.is_element_present(By.CLASS_NAME, "o_navbar_apps_menu")
        else:
            return False

    def _show_user_menu(self):
        """
        Internal method to show the user menu.
        :return: None
        """
        user_menu_class = "o_user_menu"
        menu_button = self.find_element(By.CLASS_NAME, user_menu_class)
        menu_button.click()
        time.sleep(0.5)

    def show_logout_button(self):
        """
        Internal method to show the logout button.
        :return: None
        """
        self._show_user_menu()
        expanded_menu = self.find_element(By.CLASS_NAME, "o-dropdown--menu")
        expanded_menu.click()
        time.sleep(0.5)
        self.driver.save_screenshot("login_logout_button_displayed.png")

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
        if self.is_logout_button_available():
            self.find_element(By.LINK_TEXT, "Log out").click()
            self.driver.save_screenshot("login_logout_result.png")
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
        """
        Search the page for the error element
        :return: the alert element, otherwise None
        """
        if self.is_element_present(By.CLASS_NAME, "alert"):
            return self.find_element(By.CLASS_NAME, "alert")
        else:
            return None

    def navigate_to_om_hospital_patients_homepage(self, patient_type="patients"):
        """
        Navigate to the om_hospital patients homepage
        :param patient_type:
        :return:
        """
        target_id = self.patient_id_mapping[patient_type]["action_id"]
        url = f"http://odoo-server:8069/web#cids=1&menu_id=268&action={target_id}&model=hospital.patient&view_type=list"
        self.navigate_to_url(url)
        self.driver.save_screenshot("om_hospital_patients_homepage.png")
        time.sleep(1)

    def navigate_to_om_hospital_create_patient(self):
        """
        Navigate to the create patient page by navigating to the home page and clicking on the add button
        :return: None
        """
        self.find_element(By.CLASS_NAME, "o_list_button_add").click()
        self.driver.save_screenshot("om_hospital_patients_create_patients.png")
        time.sleep(2)

    def submit_patient_info(self, patient_data):
        """
        Submits the form for creating a patient
        :param patient_data: dict containing the required fields
        :return: True if created successfully, False if patient name already exists
        """
        # use xpath because the id is dynamic
        xpath_name = "/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[1]/td[2]/input"
        xpath_age = "/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[3]/td[2]/input"
        xpath_description = "/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div[4]/table[2]/tbody/tr[2]/td[2]/textarea[1]"

        self.update_form_field_by_xpath(xpath_name, patient_data["name"])
        self.update_form_field_by_xpath(xpath_age, patient_data["age"])
        self.update_form_field_by_xpath(xpath_description, patient_data["description"])
        self.update_dropdown_menu_choice(By.NAME, "gender", f'"{patient_data["gender"]}"')
        # skip repsonsible field for now

        self.driver.save_screenshot(f"om_hospital_patients_patient_info_{patient_data['name']}.png")
        self.find_element(By.CLASS_NAME, "o_form_button_save").click()
        time.sleep(1)
        duplicates = self.find_elements(By.CLASS_NAME, "modal-footer")
        time.sleep(1)
        if len(duplicates) == 0:
            self.driver.save_screenshot(f"om_hospital_patients_patient_info_{patient_data['name']}_result.png")
            return True
        else:
            self.driver.save_screenshot(f"om_hospital_patients_patient_info_{patient_data['name']}_duplicate_result.png")
            duplicates[0].find_element(By.CLASS_NAME, "btn").click()
            time.sleep(1)
            return False

    def get_all_patients(self):
        """
        Return all patient data displayed on the om_hospital patients homepage
        :return:
        """
        parsed_patients = {}
        patients = self.find_element(By.CLASS_NAME, "o_list_table").find_elements(By.CLASS_NAME, "o_data_row")
        for patient_element in patients:
            parsed_patients[patient_element.find_element(By.NAME, "name").text] = {
                "name": patient_element.find_element(By.NAME, "name").text,
                "age": patient_element.find_element(By.NAME, "age").text,
                "gender": patient_element.find_element(By.NAME, "gender").text.lower(),
                "description": patient_element.find_element(By.NAME, "note").text
            }
        return parsed_patients

    def get_patient_data(self, name):
        """
        Get the patient record based on their name
        :param name: name of the patient
        :return: a dict containing the patient record
        """
        return self.get_all_patients()[name]

    def navigate_to_fleet_homepage(self):
        """
        Navigate to the home page of the fleet app with a list view
        :return:
        """
        url = "http://odoo-server:8069/web#cids=1&menu_id=332&action=437&model=fleet.vehicle&view_type=list"
        self.navigate_to_url(url)
        self.navigate_to_url(url)
        time.sleep(5)
        self.driver.save_screenshot("fleet_homepage_list_view.png")

    def navigate_to_fleet_create_vehicle_order(self):
        """
        Navigate to the fleet home page and
        :return:
        """
        self.find_element(By.CLASS_NAME, "o_cp_bottom_left").find_element(By.CLASS_NAME, "o_list_button_add").click()
        self.driver.save_screenshot("fleet_create_vehicle_order.png")
        time.sleep(1)

    def submit_vehicle_order_info(self, vehicle_data):
        """
        Submit vehice order with input data
        :param vehicle_data: dict containing vehicle order data
        :return: None
        """
        screenshot_name = "fleet"

        if "model_id" in vehicle_data:
            input_box = self.find_element(By.CLASS_NAME, "oe_title")\
                .find_element(By.NAME, "model_id")\
                .find_element(By.CLASS_NAME, "o_input")
            screenshot_name += f"_{vehicle_data['model_id']}"
            self.update_form_field_with_element(input_box, vehicle_data["model_id"])
        if "license_plate" in vehicle_data:
            screenshot_name += f"_{vehicle_data['license_plate']}"
            self.update_form_field_by_element_name("license_plate", vehicle_data["license_plate"])

        self.driver.save_screenshot(screenshot_name + ".png")
        self.find_element(By.CLASS_NAME, "o_form_button_save").click()
        time.sleep(0.5)
        self.driver.save_screenshot(screenshot_name + "_result.png")
        time.sleep(1)

    def get_all_vehicles(self):
        """
        Get all vehicle orders displayed on fleet homepage with the list view
        :return: dict of all vehicles current on the page
        """
        parsed_vehicles = {}
        vehicles = self.find_element(By.CLASS_NAME, "o_list_table").find_elements(By.CLASS_NAME, "o_data_row")
        for vehicle_element in vehicles:
            parsed_vehicles[vehicle_element.find_element(By.NAME, "license_plate").text] = {
                "license_plate": vehicle_element.find_element(By.NAME, "license_plate").text,
                "model_id": vehicle_element.find_element(By.NAME, "model_id").text,
            }
        print(parsed_vehicles)
        return parsed_vehicles

    def get_vehicle_data(self, license_plate):
        """
        Get the vehicle order based on the license plate
        :param license_plate: license plate number
        :return: dict of the vehicle order record
        """
        return self.get_all_vehicles().get(license_plate)
