from django.urls import path
from .views import AdminSendNotificationView

urlpatterns = [
    path('send-notification', AdminSendNotificationView.as_view(), name='admin-send-notification'),
]
