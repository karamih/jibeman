from django.urls import path
from .views import RecentJoinedUsersView, RecentActiveUsersView

urlpatterns = [
    path('recent-users-count', RecentJoinedUsersView.as_view(), name='recent-users-count'),
    path('recent-active-users-count', RecentActiveUsersView.as_view(), name='recent-active-users-count'),
]
