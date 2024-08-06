from rest_framework import serializers
from .models import NotificationModel
from client_auth.models import UserModel, ProfileModel
from utils.send_notification import send_fcm_notification


class AdminNotificationSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, required=False)
    send_to_all = serializers.BooleanField(default=False)

    class Meta:
        model = NotificationModel
        fields = ['title', 'message', 'expires_at', 'users', 'send_to_all']

    def validate(self, data):
        if not data.get('users') and not data.get('send_to_all'):
            raise serializers.ValidationError('کاربر دربافت کننده اطلاعیه را مشخص نکرده اید.')
        return data

    def create(self, validated_data):
        users = validated_data.pop('users', [])
        send_to_all = validated_data.pop('send_to_all', False)

        profiles = ProfileModel.objects.all() if send_to_all else ProfileModel.objects.filter(user__in=users)

        notifications = [
            NotificationModel(profile=profile, **validated_data)
            for profile in profiles
        ]
        NotificationModel.objects.bulk_create(notifications)

        for profile in profiles:
            try:
                status_code, response = send_fcm_notification(
                    token=profile.user.fcm_token,
                    title=validated_data['title'],
                    body=validated_data['message']
                )
                if status_code != 200:
                    raise serializers.ValidationError(f"Failed to send notification: {response}")
            except Exception as e:
                raise serializers.ValidationError(f"Error sending notification to {profile.user.phone_number}: {e}")

        return notifications[0]
