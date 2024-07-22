from rest_framework import serializers
from client_auth.models import UserModel


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['user_id', 'phone_number', 'is_active']
        read_only_fields = ['user_id', 'phone_number', 'is_active']


class AdminUserActiveSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = UserModel
        fields = ['is_active']
