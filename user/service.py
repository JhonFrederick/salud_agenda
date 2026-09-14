from typing import Optional

from django.db import transaction

from .models import AdminProfile, MedicProfile, PatientProfile, User


@transaction.atomic
def create_admin_user(
    *,
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
    **extra_fields,
) -> User:
    """
    Creates a new user with the ADMIN role and creates an associated AdminProfile.
    """
    user: User = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=User.Role.ADMIN,
        **extra_fields,
    )
    user.set_password(password)
    user.save()
    AdminProfile.objects.create(user=user)
    return user


@transaction.atomic
def create_medic_user(
    *,
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
    license_number: str = "",
    specialty: str = "",
    **extra_fields,
) -> User:
    """
    Creates a new user with the MEDIC role and creates an associated MedicProfile.
    """
    user: User = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=User.Role.MEDIC,
        **extra_fields,
    )
    user.set_password(password)
    user.save()
    MedicProfile.objects.create(
        user=user,
        license_number=license_number,
        specialty=specialty,
    )
    return user


@transaction.atomic
def create_patient_user(
    *,
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
    date_of_birth: Optional[object] = None,
    phone_number: str = "",
    **extra_fields,
) -> User:
    """
    Creates a new user with the PATIENT role and creates an associated PatientProfile.
    """
    user: User = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=User.Role.PATIENT,
        **extra_fields,
    )
    user.set_password(password)
    user.save()
    PatientProfile.objects.create(
        user=user,
        date_of_birth=date_of_birth,
        phone_number=phone_number,
    )
    return user
