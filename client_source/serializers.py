from rest_framework import serializers
from django.db import IntegrityError
from .models import FinancialSourceModel


class FinancialSourceSerializer(serializers.ModelSerializer):
    is_calculate = serializers.BooleanField(default=True)
    is_enable = serializers.BooleanField(default=True)
    card_number = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    icon_name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    icon_color = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = FinancialSourceModel
        fields = ['id', 'name', 'type', 'card_number', 'icon_name', 'icon_color', 'is_calculate', 'is_enable', 'remain',
                  'created_time', 'updated_time', 'account']
        read_only_fields = ['id', 'created_time', 'updated_time']

    def validate(self, data):
        name = data.get('name')
        source_type = data.get('type')
        card_number = data.get('card_number')
        icon_name = data.get('icon_name')
        icon_color = data.get('icon_color')
        account = data.get('account')

        current_instance_id = self.instance.id if self.instance else None

        if source_type == 'Card':
            if not card_number:
                raise serializers.ValidationError(
                    {'card_number': 'وقتی منبع مالی کارت بانکی است، شماره کارت الزامی است.'})
            if icon_name:
                raise serializers.ValidationError(
                    {'icon_name': 'وقتی منبع مالی کارت بانکی است، نام آیکون نباید ارسال شود.'})
            if icon_color:
                raise serializers.ValidationError(
                    {'icon_color': 'وقتی منبع مالی کارت بانکی است، رنگ آیکون نباید ارسال شود.'})
        elif source_type == 'Cash':
            if card_number:
                raise serializers.ValidationError(
                    {'card_number': 'وقتی منبع مالی پول نقد است، شماره کارت نباید ارسال شود.'})
            if not icon_name:
                raise serializers.ValidationError({'icon_name': 'وقتی منبع مالی پول نقد است، نام آیکون الزامی است.'})
            if not icon_color:
                raise serializers.ValidationError({'icon_color': 'وقتی منبع مالی پول نقد است، رنگ آیکون الزامی است.'})

        if FinancialSourceModel.objects.filter(name=name, account=account).exclude(id=current_instance_id).exists():
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
