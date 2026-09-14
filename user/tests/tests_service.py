from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import AdminProfile, MedicProfile, PatientProfile
from user.service import (
    create_admin_user,
    create_medic_user,
    create_patient_user,
)

User = get_user_model()


class UserServiceTests(TestCase):
    def test_create_admin_user(self):
        user = create_admin_user(
            username="admin_test",
            password="StrongPassword123!",
            email="admin@test.com",
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(user.username, "admin_test")
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertTrue(AdminProfile.objects.filter(user=user).exists())

    def test_create_medic_user(self):
        user = create_medic_user(
            username="medic_test",
            password="StrongPassword123!",
            email="medic@test.com",
            license_number="MED-12345",
            specialty="Cardiology",
        )
        self.assertEqual(user.username, "medic_test")
        self.assertEqual(user.role, User.Role.MEDIC)
        self.assertTrue(user.check_password("StrongPassword123!"))
        profile = MedicProfile.objects.get(user=user)
        self.assertEqual(profile.license_number, "MED-12345")
        self.assertEqual(profile.specialty, "Cardiology")

    def test_create_patient_user(self):
        user = create_patient_user(
            username="patient_test",
            password="StrongPassword123!",
            email="patient@test.com",
            date_of_birth="1990-01-01",
            phone_number="1234567890",
        )
        self.assertEqual(user.username, "patient_test")
        self.assertEqual(user.role, User.Role.PATIENT)
        self.assertTrue(user.check_password("StrongPassword123!"))
        profile = PatientProfile.objects.get(user=user)
        self.assertEqual(str(profile.date_of_birth), "1990-01-01")
        self.assertEqual(profile.phone_number, "1234567890")
