from rest_framework import serializers

from admin_bank.serializers import TransactionTypeSerializer
from admin_bank.models import BankModel


class BankWithTransactionsSerializer(serializers.ModelSerializer):
    transaction_types = TransactionTypeSerializer(many=True, read_only=True)

    class Meta:
        model = BankModel
        fields = ['id', 'name', 'numbers', 'created_time', 'updated_time', 'transaction_types']
