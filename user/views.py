from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AdminCreateSerializer,
    MedicCreateSerializer,
    PatientCreateSerializer,
)
from .service import (
    create_admin_user,
    create_medic_user,
    create_patient_user,
)

# TODO: Add permission classes


class AdminCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=["Users"],
        summary="Create an admin user",
        description="Registers a new user with the ADMIN role and creates an associated AdminProfile.",
        request=AdminCreateSerializer,
        responses={status.HTTP_201_CREATED: AdminCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = AdminCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_admin_user(**serializer.validated_data)
        response_serializer = AdminCreateSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MedicCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=["Users"],
        summary="Create a medic user",
        description="Registers a new user with the MEDIC role and creates an associated MedicProfile.",
        request=MedicCreateSerializer,
        responses={status.HTTP_201_CREATED: MedicCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = MedicCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_medic_user(**serializer.validated_data)
        response_serializer = MedicCreateSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PatientCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=["Users"],
        summary="Create a patient user",
        description="Registers a new user with the PATIENT role and creates an associated PatientProfile.",
        request=PatientCreateSerializer,
        responses={status.HTTP_201_CREATED: PatientCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = PatientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_patient_user(**serializer.validated_data)
        response_serializer = PatientCreateSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
