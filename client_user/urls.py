from django.urls import path

from .views import GenerateOtpView, VerifyOtpView, MockAuthentication
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('otp/generate', GenerateOtpView.as_view(), name='generate-otp'),
    path('otp/verify', VerifyOtpView.as_view(), name='verify-otp'),
    path('mock', MockAuthentication.as_view()),

    path('RefreshToken', TokenRefreshView.as_view(), name='token_refresh'),
]