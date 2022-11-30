from odoo.tests.common import TransactionCase
from odoo.tests import common, new_test_user
from odoo.exceptions import UserError

class TestLogServices(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_user = new_test_user(self.env, 'test base user', groups='base.group_user')
        self.BrandObject = self.env['fleet.vehicle.model.brand']
        self.ModelObject = self.env['fleet.vehicle.model']
        self.VehicleObject = self.env['fleet.vehicle']
        self.LogServicesObject = self.env['fleet.vehicle.log.services']

    def test_create(self):
        brand = self.BrandObject.create({
            "name": "Honda",
        })

        model = self.ModelObject.create({
            "brand_id": brand.id,
            "name": "Civic",
        })

        car_1 = self.VehicleObject.create({
            "model_id": model.id,
            "driver_id": self.base_user.partner_id.id
        })

        log_service_1 = self.LogServicesObject.create({
            'vehicle_id': car_1.id,
            'odometer': 1.0
        })
        self.assertTrue(log_service_1.odometer_id.id)

        car_2 = self.VehicleObject.create({
            "model_id": model.id,
            "driver_id": self.base_user.partner_id.id
        })
        log_service_2 = self.LogServicesObject.create({
            'vehicle_id': car_2.id,
            'odometer': 0.1
        })
        self.assertTrue(log_service_2.odometer_id.id)

        car_3 = self.VehicleObject.create({
            "model_id": model.id,
            "driver_id": self.base_user.partner_id.id
        })
        log_service_3 = self.LogServicesObject.create({
            'vehicle_id': car_3.id,
            'odometer': 0.0
        })
        self.assertFalse(log_service_3.odometer_id.id)

    def test_cant_empty_odometer(self):
        brand = self.BrandObject.create({
            "name": "Honda",
        })

        model = self.ModelObject.create({
            "brand_id": brand.id,
            "name": "Civic",
        })

        car_1 = self.VehicleObject.create({
            "model_id": model.id,
            "driver_id": self.base_user.partner_id.id
        })

        log_service_1 = self.LogServicesObject.create({
            'vehicle_id': car_1.id,
            'odometer': 1.0
        })

        self.assertEqual(log_service_1.odometer, 1.0)

        # Attempt to 0 out the odometer, catch exception
        with self.assertRaises(UserError):
            log_service_1.odometer = 0

