from django.urls import path
from .views import ClientListNotificationView

urlpatterns = [
    path('notifications', ClientListNotificationView.as_view(), name='client-list-notifications'),
]
