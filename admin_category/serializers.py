from rest_framework import serializers
from .models import DefaultCategoryModel


class DefaultCategorySerializer(serializers.ModelSerializer):
    is_default = serializers.BooleanField(default=True)

    class Meta:
        model = DefaultCategoryModel
        fields = ['id', 'name', 'transaction_type', 'is_default', 'created_time', 'updated_time']
        read_only_fields = ['id', 'created_time', 'updated_time']

    def validate(self, data):
        name = data.get('name')
        transaction_type = data.get('transaction_type')
        is_default = data.get('is_default')

        if self.instance:
            current_instance_id = self.instance.id
        else:
            current_instance_id = None

        if DefaultCategoryModel.objects.filter(name=name, transaction_type=transaction_type,
                                               is_default=is_default).exclude(id=current_instance_id).exists():
            raise serializers.ValidationError({'name': 'دسته بندی با این نام و نوع تراکنش موجود است.'})

        return data
