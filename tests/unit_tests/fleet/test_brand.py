from odoo.tests.common import TransactionCase
from odoo.tests import common, new_test_user

class TestBrand(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_user = new_test_user(self.env, 'test base user', groups='base.group_user')
        self.BrandObject = self.env['fleet.vehicle.model.brand']
        self.ModelObject = self.env['fleet.vehicle.model']
        self.VehicleObject = self.env['fleet.vehicle']

    def test_compute_correct_model_count(self):
        honda = self.BrandObject.create({
            "name": "Honda",
        })

        toyota = self.BrandObject.create({
            "name": "Toyota",
        })

        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 0), ('id', '=', honda.id)])
        self.assertEqual(res, honda)
        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 0), ('id', '=', toyota.id)])
        self.assertEqual(res, toyota)

        model_1 = self.ModelObject.create({
            "brand_id": honda.id,
            "name": "Civic",
        })

        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 1), ('id', '=', honda.id)])
        self.assertEqual(res, honda)
        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 0), ('id', '=', toyota.id)])
        self.assertEqual(res, toyota)

        model_2 = self.ModelObject.create({
            "brand_id": honda.id,
            "name": "Accord",
        })
        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 2), ('id', '=', honda.id)])
        self.assertEqual(res, honda)
        res = self.env["fleet.vehicle.model.brand"].search([('model_count', '=', 0), ('id', '=', toyota.id)])
        self.assertEqual(res, toyota)

