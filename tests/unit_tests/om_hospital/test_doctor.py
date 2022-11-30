from odoo.tests.common import TransactionCase

class TestDoctor(TransactionCase):
    def setUp(self):
        super().setUp()
        self.DoctorModelObject = self.env['hospital.doctor']

    def test_copy_without_default(self):
        default_fields = {
            'doctor_name': 'Roberts',
            'age': '40',
            'gender': 'male',
            'note': "An original note",
            'image': b'deadbeef',
            'appointment_count': "2"
        }

        doctor = self.DoctorModelObject.create(default_fields)
        doctor_copy = doctor.copy()

        self.assertNotEqual(doctor.doctor_name, doctor_copy.doctor_name)
        self.assertNotEqual(doctor.age, doctor_copy.age)
        self.assertEqual(doctor.gender, doctor_copy.gender)
        self.assertNotEqual(doctor.note, doctor_copy.note)
        self.assertEqual(doctor.image, doctor_copy.image)
        self.assertEqual(doctor.appointment_count, doctor_copy.appointment_count)

    def test_copy_with_default(self):
        default_fields = {
            'doctor_name': 'Roberts',
            'age': '40',
            'gender': 'male',
            'note': "An original note",
            'image': b'deadbeef',
            'appointment_count': "2"
        }

        doctor = self.DoctorModelObject.create(default_fields)
        doctor_copy = doctor.copy(default_fields)

        self.assertEqual(doctor.doctor_name, doctor_copy.doctor_name)
        self.assertEqual(doctor.age, doctor_copy.age)
        self.assertEqual(doctor.gender, doctor_copy.gender)
        self.assertNotEqual(doctor.note, doctor_copy.note) # note will always be different
        self.assertEqual(doctor.image, doctor_copy.image)
        self.assertEqual(doctor.appointment_count, doctor_copy.appointment_count)



