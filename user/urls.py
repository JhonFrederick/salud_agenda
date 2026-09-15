from django.urls import path

from .views import (
    AdminCreateAPIView,
    MedicCreateAPIView,
    PatientCreateAPIView,
)

urlpatterns = [
    path("admin/", AdminCreateAPIView.as_view(), name="admin-create"),
    path("medic/", MedicCreateAPIView.as_view(), name="medic-create"),
    path("patient/", PatientCreateAPIView.as_view(), name="patient-create"),
]
