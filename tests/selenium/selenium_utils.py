from pathlib import Path

from selenium import webdriver

class OdooWebDriver:
    urls = {
        "login": "http://odoo-server:8069/web/login",

    }
    def __init__(self):
        chrome_driver_path = Path("./drivers/chromedriver")
        self.driver = webdriver.Chrome(str(chrome_driver_path))

    def login(self):
        pass

    def logout(self):
        pass


class OdooHospitalAdmin(OdooWebDriver):
    def __init__(self):
        super().__init__()

    def navigate_to_hospital_app(self):
        pass


    def create_patient(self, args):
        pass

    def remove_patient(self, args):
        pass

    def update_patient(self, args):
        pass

    def get_patient_metadata(self):
        pass

    def create_patient_appointment(self, args):
        pass

    def update_patient_appointment(self, args):
        pass

    def create_doctor(self, args):
        pass


class OdooFleetAdmin(OdooWebDriver):
    def __init__(self):
        super().__init__()

    def navigate_to_fleet_app(self):
        pass

    def create_fleet_group(self, args):
        pass

    def remove_fleet_group(self, args):
        pass

    def add_fleet_vehicle(self, args):
        pass

    def remove_fleet_vehicle(self, args):
        pass