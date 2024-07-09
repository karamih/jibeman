from django.urls import path

from .views import GenerateOtpView

urlpatterns = [
    path('otp/generate', GenerateOtpView.as_view(), name='generate-otp'),
]