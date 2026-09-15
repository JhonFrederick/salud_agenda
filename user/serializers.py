from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import AdminProfile, MedicProfile, PatientProfile, User
from .service import create_admin_user, create_medic_user, create_patient_user


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ("id",)


class MedicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicProfile
        fields = ("id", "license_number", "specialty")


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ("id", "date_of_birth", "phone_number")


class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    admin_profile = AdminProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "admin_profile",
        )
        read_only_fields = ("id", "role")

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict):
        return create_admin_user(**validated_data)


class MedicCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    license_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        write_only=True,
    )
    specialty = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        write_only=True,
    )
    medic_profile = MedicProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "license_number",
            "specialty",
            "medic_profile",
        )
        read_only_fields = ("id", "role")

    def to_internal_value(self, data: dict):
        data_copy = data.copy() if hasattr(data, "copy") else dict(data)
        if "medic_profile" in data_copy and isinstance(data_copy["medic_profile"], dict):
            profile_data = data_copy["medic_profile"]
            if "license_number" in profile_data and "license_number" not in data_copy:
                data_copy["license_number"] = profile_data["license_number"]
            if "specialty" in profile_data and "specialty" not in data_copy:
                data_copy["specialty"] = profile_data["specialty"]
        return super().to_internal_value(data_copy)

    def validate_password(self, value: str):
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        return create_medic_user(**validated_data)


class PatientCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    date_of_birth = serializers.DateField(
        required=False,
        allow_null=True,
        write_only=True,
    )
    phone_number = serializers.CharField(
        max_length=30,
        required=False,
        allow_blank=True,
        write_only=True,
    )
    patient_profile = PatientProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "date_of_birth",
            "phone_number",
            "patient_profile",
        )
        read_only_fields = ("id", "role")

    def to_internal_value(self, data: dict):
        data_copy = data.copy() if hasattr(data, "copy") else dict(data)
        if "patient_profile" in data_copy and isinstance(data_copy["patient_profile"], dict):
            profile_data = data_copy["patient_profile"]
            if "date_of_birth" in profile_data and "date_of_birth" not in data_copy:
                data_copy["date_of_birth"] = profile_data["date_of_birth"]
            if "phone_number" in profile_data and "phone_number" not in data_copy:
                data_copy["phone_number"] = profile_data["phone_number"]
        return super().to_internal_value(data_copy)

    def validate_password(self, value: str):
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        return create_patient_user(**validated_data)
