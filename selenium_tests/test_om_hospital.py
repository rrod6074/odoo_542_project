import time

from selenium.webdriver.common.by import By

from selenium_utils import SeleniumBaseTestCase


class OmHospitalBaseTestCase(SeleniumBaseTestCase):
    def setUp(self):
        super().setUp()
        self.odoo_selenium_util.login("admin", "admin")

    def tearDown(self):
        self.odoo_selenium_util.logout()
        super().tearDown()


class OdooOmHospitalPatientInteraction(OmHospitalBaseTestCase):
    def setUp(self):
        super().setUp()
        self.odoo_selenium_util.navigate_to_om_hospital_patients_homepage("patients")

    def test_navigate_to_om_hospital_patients(self):
        """
        positive test case:
        login and enter the odoo homepage
        navigate to om_hospital homepage
        checks for expected text from application's home page
        """
        response_text = self.odoo_selenium_util.find_element(By.CLASS_NAME, "text-900").text
        expected_text = self.odoo_selenium_util.patient_id_mapping["patients"]["text"]
        self.assertEqual(response_text, expected_text)

    def test_add_new_valid_patient_info(self):
        """
        positive test case:
        login and enters the odoo homepage
        navigate with button clicks to create patient page
        adds a patient with a unique identifier
        checks for the patient name and matching data from om_hospital patient homepage
        """
        test_patient_data = {
            "name": f"selenium_patient_{str(int(time.time()))}",
            "age": "44",
            "gender": "female",
            "description": "words go here",
        }
        self.odoo_selenium_util.navigate_to_om_hospital_create_patient()
        self.odoo_selenium_util.submit_patient_info(test_patient_data)
        self.odoo_selenium_util.navigate_to_om_hospital_patients_homepage("patients")
        result = self.odoo_selenium_util.get_patient_data(test_patient_data["name"])
        self.assertDictEqual(result, test_patient_data)

    def test_add_duplicate_patient_info(self):
        """
        negative test case:
        login and enters the odoo homepage
        navigate with button clicks to create a patient with a unique identifier
        navigate with button clicks to create duplicate patient
        checks for reported failure to create patient based on pop up
        """
        test_patient_data = {
            "name": f"selenium_patient_{str(int(time.time()))}",
            "age": "44",
            "gender": "female",
            "description": str(int(time.time())),
        }
        self.odoo_selenium_util.navigate_to_om_hospital_create_patient()
        self.odoo_selenium_util.submit_patient_info(test_patient_data)
        self.odoo_selenium_util.navigate_to_om_hospital_patients_homepage("patients")
        self.odoo_selenium_util.navigate_to_om_hospital_create_patient()
        result = self.odoo_selenium_util.submit_patient_info(test_patient_data)
        self.assertFalse(result)

    def tearDown(self):
        # todo: delete test patient records
        super().tearDown()
