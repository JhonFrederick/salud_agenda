import pytest
from django.contrib.auth import get_user_model

from user.models import AdminProfile, MedicProfile, PatientProfile
from user.service import (
    create_admin_user,
    create_medic_user,
    create_patient_user,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserService:
    def test_create_admin_user(self):
        admin_data: dict = {
            "username": "admin_test",
            "password": "StrongPassword123!",
            "email": "admin@test.com",
            "first_name": "Admin",
            "last_name": "User",
        }
        user: User = create_admin_user(**admin_data)
        assert user.username == "admin_test"
        assert user.role == User.Role.ADMIN
        assert user.check_password("StrongPassword123!")
        assert AdminProfile.objects.filter(user=user).exists()

    def test_create_medic_user(self):
        medic_data: dict = {
            "username": "medic_test",
            "password": "StrongPassword123!",
            "email": "medic@test.com",
            "license_number": "MED-12345",
            "specialty": "Cardiology",
        }

        user: User = create_medic_user(**medic_data)
        assert user.username == "medic_test"
        assert user.role == User.Role.MEDIC
        assert user.check_password("StrongPassword123!")
        profile = MedicProfile.objects.get(user=user)
        assert profile.license_number == "MED-12345"
        assert profile.specialty == "Cardiology"

    def test_create_patient_user(self):
        patient_data: dict = {
            "username": "patient_test",
            "password": "StrongPassword123!",
            "email": "patient@test.com",
            "date_of_birth": "1990-01-01",
            "phone_number": "1234567890",
        }
        user: User = create_patient_user(**patient_data)
        assert user.username == "patient_test"
        assert user.role == User.Role.PATIENT
        assert user.check_password("StrongPassword123!")
        profile = PatientProfile.objects.get(user=user)
        assert str(profile.date_of_birth) == "1990-01-01"
        assert profile.phone_number == "1234567890"
