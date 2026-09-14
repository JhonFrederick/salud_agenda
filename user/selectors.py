from typing import Optional
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import AdminProfile, MedicProfile, PatientProfile, User


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Retrieves a user by ID.
    """
    return User.objects.filter(id=user_id).first()


def get_user_with_profile(user_id: int) -> Optional[User]:
    """
    Retrieves a user by ID with their corresponding profile pre-selected.
    """
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None
    if user.role == User.Role.ADMIN:
        return User.objects.select_related('admin_profile').filter(id=user_id).first()
    elif user.role == User.Role.MEDIC:
        return User.objects.select_related('medic_profile').filter(id=user_id).first()
    elif user.role == User.Role.PATIENT:
        return User.objects.select_related('patient_profile').filter(id=user_id).first()
    return user


def list_users(
    *,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> QuerySet[User]:
    """
    Lists users filtered by role and active status.
    """
    qs = User.objects.all()
    if role is not None:
        qs = qs.filter(role=role)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs


def list_medics(
    *,
    specialty: Optional[str] = None,
    is_active: Optional[bool] = True,
) -> QuerySet[User]:
    """
    Lists medic users with their profiles, optionally filtered by specialty.
    """
    qs = User.objects.filter(role=User.Role.MEDIC).select_related('medic_profile')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if specialty:
        qs = qs.filter(medic_profile__specialty__icontains=specialty)
    return qs


def list_patients(*, is_active: Optional[bool] = True) -> QuerySet[User]:
    """
    Lists patient users with their profiles.
    """
    qs = User.objects.filter(role=User.Role.PATIENT).select_related('patient_profile')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs


def list_admins(*, is_active: Optional[bool] = True) -> QuerySet[User]:
    """
    Lists admin users with their profiles.
    """
    qs = User.objects.filter(role=User.Role.ADMIN).select_related('admin_profile')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs


def get_medic_profile_by_user_id(user_id: int) -> Optional[MedicProfile]:
    """
    Retrieves the MedicProfile for a given user ID.
    """
    return MedicProfile.objects.select_related('user').filter(user_id=user_id).first()


def get_patient_profile_by_user_id(user_id: int) -> Optional[PatientProfile]:
    """
    Retrieves the PatientProfile for a given user ID.
    """
    return PatientProfile.objects.select_related('user').filter(user_id=user_id).first()


def get_admin_profile_by_user_id(user_id: int) -> Optional[AdminProfile]:
    """
    Retrieves the AdminProfile for a given user ID.
    """
    return AdminProfile.objects.select_related('user').filter(user_id=user_id).first()
