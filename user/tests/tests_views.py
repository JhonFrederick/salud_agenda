import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from conftest import TestBase
from user.models import MedicProfile, PatientProfile

User = get_user_model()


class TestUserAPIView(TestBase):
    @pytest.fixture
    def admin_payload(self):
        return {
            "username": "api_admin",
            "email": "api_admin@example.com",
            "password": "StrongPassword123!",
            "first_name": "Super",
            "last_name": "Admin",
        }

    @pytest.fixture
    def medic_payload(self):
        return {
            "username": "api_medic",
            "email": "api_medic@example.com",
            "password": "StrongPassword123!",
            "first_name": "Doctor",
            "last_name": "House",
            "license_number": "LIC-1001",
            "specialty": "Diagnostics",
        }

    @pytest.fixture
    def patient_payload(self):
        return {
            "username": "api_patient",
            "email": "api_patient@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1992-03-20",
            "phone_number": "555-4321",
        }

    def test_create_admin_view(self, admin_payload):
        response = self.client.post("/api/users/admin/", admin_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "api_admin"
        assert response.data["role"] == User.Role.ADMIN
        assert "admin_profile" in response.data
        assert User.objects.filter(username="api_admin", role=User.Role.ADMIN).exists()

    def test_create_medic_view(self, medic_payload):
        response = self.client.post("/api/users/medic/", medic_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "api_medic"
        assert response.data["role"] == User.Role.MEDIC
        assert "medic_profile" in response.data
        assert response.data["medic_profile"]["license_number"] == "LIC-1001"
        assert response.data["medic_profile"]["specialty"] == "Diagnostics"
        assert MedicProfile.objects.filter(license_number="LIC-1001").exists()

    def test_create_patient_view(self, patient_payload):
        response = self.client.post("/api/users/patient/", patient_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "api_patient"
        assert response.data["role"] == User.Role.PATIENT
        assert "patient_profile" in response.data
        assert response.data["patient_profile"]["phone_number"] == "555-4321"
        assert PatientProfile.objects.filter(phone_number="555-4321").exists()

    @pytest.mark.parametrize(
        ("path", "expected_status_code"),
        [
            ("/api/users/admin/", status.HTTP_400_BAD_REQUEST),
            ("/api/users/medic/", status.HTTP_400_BAD_REQUEST),
            ("/api/users/patient/", status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_invalid_payload_returns_400(self, path, expected_status_code):
        response = self.client.post(path, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
