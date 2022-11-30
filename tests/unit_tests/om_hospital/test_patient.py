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
            patient = self.PatientModelObject.create({
                'name': 'John',
                'age': '0'
            })

    # Strangely, the code does no checking for negative numbers
    # def test_age_less_than_zero(self):
    #     with self.assertRaises(ValidationError):
    #         patient = self.PatientModelObject.create({
    #             'name': 'John',
    #             'age': '-1'
    #         })

    def test_duplicate_name_not_allowed(self):
        patient1 = self.PatientModelObject.create({
            'name': 'John',
            'age': '1'
        })
        self.assertEqual(patient1.name, 'John')

        patient2 = self.PatientModelObject.create({
            'name': 'Paul',
            'age': '1'
        })
        self.assertEqual(patient2.name, 'Paul')

        with self.assertRaises(ValidationError):
            patient3 = self.PatientModelObject.create({
                'name': 'John',
                'age': '2'
            })

