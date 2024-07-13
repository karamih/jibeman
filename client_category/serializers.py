from rest_framework import serializers
from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CategoryModel
        fields = ['id', 'account', 'name', 'transaction_type', 'is_default', 'created_time', 'updated_time']
        read_only_fields = ['id', 'account', 'is_default', 'created_time', 'updated_time']

    def validate(self, data):
        account = self.context['request'].parser_context['kwargs']['account_id']
        name = data.get('name')
        transaction_type = data.get('transaction_type')

        if CategoryModel.objects.filter(name=name, account_id=account, transaction_type=transaction_type).exclude(
                id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({'name': 'دسته بندی با این نام موجود است.'})

        return data
