from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from auth.views import LoginAPIView

urlpatterns = [
    # JWT Authentication Endpoints
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
