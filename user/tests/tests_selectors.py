from django.test import TestCase

from user.models import User
from user.selectors import (
    get_admin_profile_by_user_id,
    get_medic_profile_by_user_id,
    get_patient_profile_by_user_id,
    get_user_by_id,
    get_user_with_profile,
    list_admins,
    list_medics,
    list_patients,
    list_users,
)
from user.tests.factories.user import AdminProfileFactory, MedicProfileFactory, PatientProfileFactory, UserFactory


class UserSelectorsTests(TestCase):
    def setUp(self):
        self.admin = AdminProfileFactory(user=UserFactory(
            username='admin1',
            password='Password123!',
            email='admin1@test.com',
            role=User.Role.ADMIN,
        )).user
        self.medic = MedicProfileFactory(user=UserFactory(
            username='medic1',
            password='Password123!',
            email='medic1@test.com',
            role=User.Role.MEDIC,
        ), license_number='LIC-999',
            specialty='Pediatrics', ).user
        self.patient = PatientProfileFactory(user=UserFactory(
            username='patient1',
            password='Password123!',
            email='patient1@test.com',
            role=User.Role.PATIENT,
        ), date_of_birth='1995-05-15',
            phone_number='5551234', ).user

    def test_get_user_by_id(self):
        self.assertEqual(get_user_by_id(self.admin.id), self.admin)
        self.assertIsNone(get_user_by_id(999999))

    def test_get_user_with_profile(self):
        admin_with_profile = get_user_with_profile(self.admin.id)
        self.assertIsNotNone(admin_with_profile)
        self.assertIsNotNone(admin_with_profile.admin_profile)

        medic_with_profile = get_user_with_profile(self.medic.id)
        self.assertIsNotNone(medic_with_profile)
        self.assertEqual(medic_with_profile.medic_profile.specialty, 'Pediatrics')

        patient_with_profile = get_user_with_profile(self.patient.id)
        self.assertIsNotNone(patient_with_profile)
        self.assertEqual(patient_with_profile.patient_profile.phone_number, '5551234')

    def test_list_users(self):
        self.assertEqual(list_users().count(), 3)
        self.assertEqual(list_users(role=User.Role.MEDIC).count(), 1)

    def test_list_medics(self):
        medics = list_medics(specialty='pedia')
        self.assertEqual(medics.count(), 1)
        self.assertEqual(medics.first(), self.medic)

    def test_list_patients(self):
        patients = list_patients()
        self.assertEqual(patients.count(), 1)
        self.assertEqual(patients.first(), self.patient)

    def test_list_admins(self):
        admins = list_admins()
        self.assertEqual(admins.count(), 1)
        self.assertEqual(admins.first(), self.admin)

    def test_get_profile_by_user_id(self):
        self.assertIsNotNone(get_admin_profile_by_user_id(self.admin.id))
        self.assertIsNotNone(get_medic_profile_by_user_id(self.medic.id))
        self.assertIsNotNone(get_patient_profile_by_user_id(self.patient.id))
