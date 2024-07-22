from django.urls import path
from .views import AdminUserListView, ActivateUserView

urlpatterns = [
    path('users', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/activate', ActivateUserView.as_view(), name='admin-user-activate'),
]
