from django.urls import path
from .views import AdminUserRegisterView, AdminUserLoginView

urlpatterns = [
    path('register', AdminUserRegisterView.as_view(), name='admin-register'),
    path('login', AdminUserLoginView.as_view(), name='admin-login'),
]
