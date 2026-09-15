import pytest

from conftest import TestBase
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
from user.tests.factories.user import (
    AdminProfileFactory,
    MedicProfileFactory,
    PatientProfileFactory,
    UserFactory,
)


class TestUserSelectors(TestBase):
    @pytest.fixture
    def admin(self):
        return AdminProfileFactory(
            user=UserFactory(
                username="admin1",
                password="Password123!",
                email="admin1@test.com",
                role=User.Role.ADMIN,
            )
        ).user

    @pytest.fixture
    def medic(self):
        return MedicProfileFactory(
            user=UserFactory(
                username="medic1",
                password="Password123!",
                email="medic1@test.com",
                role=User.Role.MEDIC,
            ),
            license_number="LIC-999",
            specialty="Pediatrics",
        ).user

    @pytest.fixture
    def patient(self):
        return PatientProfileFactory(
            user=UserFactory(
                username="patient1",
                password="Password123!",
                email="patient1@test.com",
                role=User.Role.PATIENT,
            )
        ).user

    def test_get_user_by_id(self, admin):
        assert get_user_by_id(admin.id) == admin
        assert get_user_by_id(999999) is None

    @pytest.mark.parametrize(
        ("fixture_name", "profile_attribute", "expected_value"),
        [
            ("admin", "admin_profile", None),
            ("medic", "medic_profile", "Pediatrics"),
            ("patient", "patient_profile", None),
        ],
    )
    def test_get_user_with_profile(
        self,
        request,
        fixture_name,
        profile_attribute,
        expected_value,
    ):
        user = request.getfixturevalue(fixture_name)

        user_with_profile = get_user_with_profile(user.id)

        assert user_with_profile is not None

        profile = getattr(user_with_profile, profile_attribute)
        assert profile is not None

        if expected_value:
            assert profile.specialty == expected_value

    def test_list_users(self, admin, patient, medic):
        assert list_users().count() == 3

    @pytest.mark.parametrize(
        ("role", "expected_count"),
        [
            (User.Role.ADMIN, 1),
            (User.Role.MEDIC, 1),
            (User.Role.PATIENT, 1),
        ],
    )
    def test_list_users_by_role(
        self,
        admin,
        patient,
        medic,
        role,
        expected_count,
    ):
        assert list_users(role=role).count() == expected_count

    def test_list_medics(self, medic):
        medics = list_medics(specialty="pedia")

        assert medics.count() == 1
        assert medics.first() == medic

    def test_list_patients(self, patient):
        patients = list_patients()

        assert patients.count() == 1
        assert patients.first() == patient

    def test_list_admins(self, admin):
        admins = list_admins()

        assert admins.count() == 1
        assert admins.first() == admin

    @pytest.mark.parametrize(
        ("fixture_name", "selector"),
        [
            ("admin", get_admin_profile_by_user_id),
            ("medic", get_medic_profile_by_user_id),
            ("patient", get_patient_profile_by_user_id),
        ],
    )
    def test_get_profile_by_user_id(
        self,
        request,
        fixture_name,
        selector,
    ):
        user = request.getfixturevalue(fixture_name)

        assert selector(user.id) is not None
