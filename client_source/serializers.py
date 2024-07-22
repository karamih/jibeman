from rest_framework import serializers
from django.db import IntegrityError
from .models import FinancialSourceModel


class FinancialSourceSerializer(serializers.ModelSerializer):
    is_calculate = serializers.BooleanField(default=True)
    is_enable = serializers.BooleanField(default=True)

    class Meta:
        model = FinancialSourceModel
        fields = ['id', 'name', 'type', 'card_number', 'is_calculate', 'is_enable', 'remain', 'created_time',
                  'updated_time', 'account']
        read_only_fields = ['id', 'created_time', 'updated_time']

    def validate(self, data):
        card_number = data.get('card_number')
        type = data.get('type')
        account = data.get('account')

        if self.instance:
            current_instance_id = self.instance.id
        else:
            current_instance_id = None

        if type == 'Card' and not card_number:
            raise serializers.ValidationError({'card_number': 'وقتی منبع مالی کارت بانکی است، شماره کارت الزامی است.'})
        elif type != 'Card' and card_number:
            raise serializers.ValidationError(
                {'card_number': 'وقتی منبع مالی پول نقد است، شماره کارت نباید ارسال شود.'})

        if FinancialSourceModel.objects.filter(name=data.get('name'), account=account).exclude(
                id=current_instance_id).exists():
            raise serializers.ValidationError({'name': 'منبع مالی با این نام برای این حساب از قبل وجود دارد.'})

        if card_number and FinancialSourceModel.objects.filter(card_number=card_number, account=account).exclude(
                id=current_instance_id).exists():
            raise serializers.ValidationError(
                {'card_number': 'منبع مالی با این شماره کارت برای این حساب از قبل وجود دارد.'})

        return data

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": "یک منبع مالی با این اطلاعات موجود است."})
