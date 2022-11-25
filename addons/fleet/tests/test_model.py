from odoo.tests.common import TransactionCase
from odoo.tests import new_test_user

class TestModel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_user = new_test_user(self.env, 'test base user', groups='base.group_user')
        self.BrandObject = self.env['fleet.vehicle.model.brand']
        self.ModelObject = self.env['fleet.vehicle.model']

    def test_verify_name(self):
        honda = self.BrandObject.create({
            "name": "Honda",
        })

        civic = self.ModelObject.create({
            "brand_id": honda.id,
            "name": "Civic",
        })

        res = civic.name_get()
        self.assertEqual(res[0][0], civic.id)
        self.assertEqual(res[0][1], honda.name + "/" + civic.name)

        nameless_brand = self.BrandObject.create({
            "name": "",
        })

        nexus = self.ModelObject.create({
            "brand_id": nameless_brand.id,
            "name": "Nexus",
        })

        res = nexus.name_get()
        self.assertEqual(res[0][0], nexus.id)
        self.assertEqual(res[0][1], nexus.name)
