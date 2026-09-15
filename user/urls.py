from django.urls import path

from .views import (
    AdminCreateView,
    MedicCreateView,
    PatientCreateView,
)

urlpatterns = [
    path("admin/", AdminCreateView.as_view(), name="admin-create"),
    path("medic/", MedicCreateView.as_view(), name="medic-create"),
    path("patient/", PatientCreateView.as_view(), name="patient-create"),
]
