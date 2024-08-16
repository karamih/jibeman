from rest_framework import serializers
from .models import AccountModel


class AccountSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = AccountModel
        fields = ['id', 'name', 'icon_name', 'icon_color', 'credit', 'is_active', 'created_time', 'updated_time']
        read_only_fields = ['id', 'credit', 'created_time', 'updated_time']
