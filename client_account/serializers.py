from rest_framework import serializers
from .models import AccountModel


class AccountSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = AccountModel
        fields = ['id', 'profile', 'name', 'credit', 'is_active', 'created_time', 'updated_time']
        read_only_fields = ['id', 'profile', 'created_time', 'updated_time']
