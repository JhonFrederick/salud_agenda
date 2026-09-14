from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from user.models import MedicProfile, PatientProfile

User = get_user_model()


class UserAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_admin_view(self):
        payload = {
            "username": "api_admin",
            "email": "api_admin@example.com",
            "password": "StrongPassword123!",
            "first_name": "Super",
            "last_name": "Admin",
        }
        response = self.client.post("/api/users/admin/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "api_admin")
        self.assertEqual(response.data["role"], User.Role.ADMIN)
        self.assertIn("admin_profile", response.data)
        self.assertTrue(User.objects.filter(username="api_admin", role=User.Role.ADMIN).exists())

    def test_create_medic_view(self):
        payload = {
            "username": "api_medic",
            "email": "api_medic@example.com",
            "password": "StrongPassword123!",
            "first_name": "Doctor",
            "last_name": "House",
            "license_number": "LIC-1001",
            "specialty": "Diagnostics",
        }
        response = self.client.post("/api/users/medic/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "api_medic")
        self.assertEqual(response.data["role"], User.Role.MEDIC)
        self.assertIn("medic_profile", response.data)
        self.assertEqual(response.data["medic_profile"]["license_number"], "LIC-1001")
        self.assertEqual(response.data["medic_profile"]["specialty"], "Diagnostics")
        self.assertTrue(MedicProfile.objects.filter(license_number="LIC-1001").exists())

    def test_create_patient_view(self):
        payload = {
            "username": "api_patient",
            "email": "api_patient@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1992-03-20",
            "phone_number": "555-4321",
        }
        response = self.client.post("/api/users/patient/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "api_patient")
        self.assertEqual(response.data["role"], User.Role.PATIENT)
        self.assertIn("patient_profile", response.data)
        self.assertEqual(response.data["patient_profile"]["phone_number"], "555-4321")
        self.assertTrue(PatientProfile.objects.filter(phone_number="555-4321").exists())

    def test_invalid_payload_returns_400(self):
        response = self.client.post("/api/users/patient/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
