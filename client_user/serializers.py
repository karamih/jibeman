from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import TOTPModel


class PhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد."
                                   )]
    )

    class Meta:
        model = TOTPModel
        fields = ['phone_number']


class OtpVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد."
                                   )]
    )

    class Meta:
        model = TOTPModel
        fields = ['phone_number', 'otp']
