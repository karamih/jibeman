from rest_framework import generics, permissions
from admin_notification.models import NotificationModel
from .serializers import ClientNotificationSerializer


class ClientListNotificationView(generics.ListAPIView):
    serializer_class = ClientNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationModel.objects.filter(profile__user=self.request.user)
