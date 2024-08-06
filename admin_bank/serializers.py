from rest_framework import serializers
from .models import BankModel, TransactionTypeModel


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankModel
        fields = ['id', 'name', 'numbers', 'created_time', 'updated_time']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTypeModel
        fields = "__all__"
