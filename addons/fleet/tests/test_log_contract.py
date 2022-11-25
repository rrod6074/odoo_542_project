from odoo.tests.common import TransactionCase
from odoo.tests import new_test_user
from odoo import fields

class TestLogContract(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_user = new_test_user(self.env, 'test base user', groups='base.group_user')
        self.BrandObject = self.env['fleet.vehicle.model.brand']
        self.ModelObject = self.env['fleet.vehicle.model']
        self.VehicleObject = self.env['fleet.vehicle']
        self.LogContractObject = self.env['fleet.vehicle.log.contract']

    def test_contract_days_left(self):
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

        log_contract_1 = self.LogContractObject.create({
            'vehicle_id': car_1.id,
            'start_date': fields.Date.add(fields.Date.today(), days=0),
            'expiration_date': fields.Date.add(fields.Date.today(), days=0)
        })
        self.assertEqual(log_contract_1.days_left, 0)

        log_contract_2 = self.LogContractObject.create({
            'vehicle_id': car_1.id,
            'start_date': fields.Date.add(fields.Date.today(), days=0),
            'expiration_date': fields.Date.add(fields.Date.today(), days=10)
        })
        self.assertEqual(log_contract_2.days_left, 10)

        log_contract_3 = self.LogContractObject.create({
            'vehicle_id': car_1.id,
            'start_date': fields.Date.add(fields.Date.today(), days=-5),
            'expiration_date': fields.Date.add(fields.Date.today(), days=10)
        })
        self.assertEqual(log_contract_3.days_left, 10)
