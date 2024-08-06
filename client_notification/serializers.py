from rest_framework import serializers

from admin_notification.models import NotificationModel


class ClientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = ['id', 'title', 'message', 'created_time']
