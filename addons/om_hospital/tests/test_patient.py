from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestPatient(TransactionCase):
    def setUp(self):
        super().setUp()
        self.PatientModelObject = self.env['hospital.patient']

    def test_age_greater_than_zero(self):
        patient = self.PatientModelObject.create({
            'name': 'John',
            'age': '1'
        })
        self.assertEqual(patient.age, 1)

    def test_age_is_zero(self):
        with self.assertRaises(ValidationError):
            self.PatientModelObject.create({
                'name': 'John',
                'age': '0'
            })


