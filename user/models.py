from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class User(BaseModel, AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Superadmin'
        ADMIN = 'ADMIN', 'Admin'
        MEDIC = 'MEDIC', 'Medic'
        PATIENT = 'PATIENT', 'Patient'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    def __str__(self):
        return self.username


class AdminProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin_profile',
    )

    def __str__(self):
        return f'Admin profile: {self.user.username}'


class MedicProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='medic_profile',
    )
    license_number = models.CharField(max_length=100, blank=True)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Medic profile: {self.user.username}'


class PatientProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'Patient profile: {self.user.username}'