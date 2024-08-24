from django.urls import path

from .views import GenerateOtpView, VerifyOtpView, UserProfileDataView, MockAuthentication, CustomTokenRefreshView


urlpatterns = [
    path('otp/generate', GenerateOtpView.as_view(), name='generate-otp'),
    path('otp/verify', VerifyOtpView.as_view(), name='verify-otp'),
    path('mock', MockAuthentication.as_view()),

    path('RefreshToken', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('user-profile', UserProfileDataView.as_view(), name='user-profile')
]