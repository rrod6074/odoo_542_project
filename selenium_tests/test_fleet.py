import time

from selenium.webdriver.common.by import By

from selenium_utils import SeleniumBaseTestCase


class FleetBaseTestCase(SeleniumBaseTestCase):
    def setUp(self):
        super().setUp()
        self.odoo_selenium_util.login("admin", "admin")

    def tearDown(self):
        self.odoo_selenium_util.logout()
        super().tearDown()


class FleetAdminInteraction(FleetBaseTestCase):
    def setUp(self):
        super().setUp()
        self.odoo_selenium_util.navigate_to_fleet_homepage()

    def test_navigate_to_fleet_homepage(self):
        """
        positive test case:
        navigates to home page of fleet
        checks for expected text from application's home page
        """
        response_text = self.odoo_selenium_util.find_element(By.CLASS_NAME, "text-900").text
        expected_text = "Vehicles"
        self.assertEqual(response_text, expected_text)

    def test_create_valid_vehicle_order(self):
        """
        positive test case:
        login and enters the odoo homepage
        navigate with button clicks to create vehicle page
        adds a vehicle with model type and license plate
        checks for the patient name and matching data from om_hospital patient homepage
        """
        test_vehicle_data = {
            "model_id": "A1",
            "license_plate": str(int(time.time()))[-7:],
        }
        self.odoo_selenium_util.navigate_to_fleet_create_vehicle_order()
        self.odoo_selenium_util.submit_vehicle_order_info(test_vehicle_data)
        self.odoo_selenium_util.navigate_to_fleet_homepage()
        test_vehicle_data["model_id"] = "Audi/A1"
        result = self.odoo_selenium_util.get_vehicle_data(test_vehicle_data["license_plate"])
        self.assertDictEqual(result, test_vehicle_data)

    def test_create_invalid_vehicle_order(self):
        """
        negative test case:
        login and enters the odoo homepage
        navigate with button clicks to create vehicle page
        adds a vehicle with only license plate, without the required field for model
        checks for reported failure to create vehicle based on pop up
        """
        test_vehicle_data = {
            "license_plate": str(int(time.time()))[-7:],
        }
        self.odoo_selenium_util.navigate_to_fleet_create_vehicle_order()
        self.odoo_selenium_util.submit_vehicle_order_info(test_vehicle_data)
        self.odoo_selenium_util.navigate_to_fleet_homepage()
        result = self.odoo_selenium_util.get_vehicle_data(test_vehicle_data["license_plate"])
        self.assertIsNone(result)
