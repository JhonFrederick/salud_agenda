from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from conftest import TestBase
from user.tests.factories.user import UserFactory

User = get_user_model()


def _create_expired_refresh_token(user) -> RefreshToken:
    token = RefreshToken.for_user(user)
    token.set_exp(lifetime=timedelta(seconds=-10))
    return token


def _create_expired_access_token(user) -> AccessToken:
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(seconds=-10))
    return token


class TestLoginAPIView(TestBase):
    @pytest.fixture
    def test_password(self) -> str:
        return "StrongAuthPass123!"

    @pytest.fixture
    def active_user(self, test_password) -> User:
        user: User = UserFactory(
            username="auth_patient",
            email="patient@authtest.com",
            password=test_password,
            role=User.Role.PATIENT,
        )
        return user

    @pytest.mark.parametrize(
        ("role", "username"),
        [
            (User.Role.PATIENT, "login_patient"),
            (User.Role.MEDIC, "login_medic"),
            (User.Role.ADMIN, "login_admin"),
            (User.Role.SUPERADMIN, "login_superadmin"),
        ],
    )
    def test_login_success_across_roles(self, role, username, test_password):
        user: User = UserFactory(
            username=username,
            email=f"{username}@example.com",
            password=test_password,
            role=role,
        )

        payload: dict = {"username": user.username, "password": test_password}
        response = self.client.post(reverse("login"), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert isinstance(response.data["access"], str) and len(response.data["access"]) > 0
        assert isinstance(response.data["refresh"], str) and len(response.data["refresh"]) > 0

    @pytest.mark.parametrize(
        ("username_input", "password_input"),
        [
            ("auth_patient", "WrongPassword!"),
            ("non_existent_user", "StrongAuthPass123!"),
            ("non_existent_user", "WrongPassword!"),
        ],
    )
    def test_login_invalid_credentials_returns_401(self, active_user: User, username_input: str, password_input: str):
        payload: dict = {"username": username_input, "password": password_input}
        response = self.client.post(reverse("login"), payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data

    def test_login_inactive_user_returns_401(self, test_password: str):
        UserFactory(
            username="inactive_user",
            email="inactive@example.com",
            password=test_password,
            is_active=False,
        )

        payload: dict = {"username": "inactive_user", "password": test_password}
        response = self.client.post(reverse("login"), payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"username": "auth_patient"},
            {"password": "StrongAuthPass123!"},
            {"username": "", "password": "StrongAuthPass123!"},
            {"username": "auth_patient", "password": ""},
            {"username": None, "password": "StrongAuthPass123!"},
            {"username": "auth_patient", "password": None},
        ],
    )
    def test_login_invalid_payload_returns_400(self, active_user: User, payload: dict):
        response = self.client.post(reverse("login"), payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
    def test_login_unsupported_http_methods(self, method):
        client_method = getattr(self.client, method)
        response = client_method(reverse("login"))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestTokenRefreshAPIView(TestBase):
    @pytest.fixture
    def user(self) -> User:
        return UserFactory(
            username="refresh_user",
            email="refresh@example.com",
            password="StrongPassword123!",
        )

    def test_token_refresh_success(self, user: User):
        refresh_token = RefreshToken.for_user(user)
        payload: dict = {"refresh": str(refresh_token)}

        response = self.client.post(reverse("token_refresh"), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert isinstance(response.data["access"], str) and len(response.data["access"]) > 0

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"refresh": ""},
            {"refresh": None},
            {"token": "some_token"},
        ],
    )
    def test_token_refresh_invalid_payload_returns_400(self, payload: dict):
        response = self.client.post(reverse("token_refresh"), payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        "token_generator",
        [
            lambda user: "invalid.jwt.token.string",
            lambda user: str(AccessToken.for_user(user)),
            lambda user: str(_create_expired_refresh_token(user)),
        ],
    )
    def test_token_refresh_invalid_or_expired_returns_401(self, user: User, token_generator):
        token_str = token_generator(user)
        payload: dict = {"refresh": token_str}

        response = self.client.post(reverse("token_refresh"), payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get("code") == "token_not_valid" or "detail" in response.data

    @pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
    def test_token_refresh_unsupported_http_methods(self, method: str):
        client_method = getattr(self.client, method)
        response = client_method(reverse("token_refresh"))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestTokenVerifyAPIView(TestBase):
    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(
            username="verify_user",
            email="verify@example.com",
            password="StrongPassword123!",
        )

    @pytest.mark.parametrize(
        "token_getter",
        [
            lambda user: str(AccessToken.for_user(user)),
            lambda user: str(RefreshToken.for_user(user)),
        ],
    )
    def test_token_verify_success(self, user: User, token_getter):
        token_str = token_getter(user)
        payload: dict = {"token": token_str}

        response = self.client.post(reverse("token_verify"), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"token": ""},
            {"token": None},
            {"refresh": "some_token"},
        ],
    )
    def test_token_verify_invalid_payload_returns_400(self, payload: dict):
        response = self.client.post(reverse("token_verify"), payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        "token_generator",
        [
            lambda user: "invalid.jwt.token.string",
            lambda user: str(_create_expired_access_token(user)),
            lambda user: str(_create_expired_refresh_token(user)),
        ],
    )
    def test_token_verify_invalid_or_expired_returns_401(self, user: User, token_generator):
        token_str = token_generator(user)
        payload: dict = {"token": token_str}

        response = self.client.post(reverse("token_verify"), payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get("code") == "token_not_valid" or "detail" in response.data

    @pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
    def test_token_verify_unsupported_http_methods(self, method: str):
        client_method = getattr(self.client, method)
        response = client_method(reverse("token_verify"))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
