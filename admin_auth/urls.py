from django.urls import path
from .views import AdminUserProfileView, AdminUserRegisterView, AdminUserLoginView, AdminUpdateUsernameView, \
    AdminUpdatePasswordView

urlpatterns = [
    path('get-profile', AdminUserProfileView.as_view(), name='admin-get-profile'),
    path('register', AdminUserRegisterView.as_view(), name='admin-register'),
    path('login', AdminUserLoginView.as_view(), name='admin-login'),
    path('update-username', AdminUpdateUsernameView.as_view(), name='admin-update-username'),
    path('update-password', AdminUpdatePasswordView.as_view(), name='admin-update-password'),
]
