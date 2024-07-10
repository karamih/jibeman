from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TOTPModel, ProfileModel

UserModel = get_user_model()


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
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد.")]
    )
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = TOTPModel
        fields = ['phone_number', 'otp']

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        otp_code = attrs.get('otp')

        try:
            user_otp_instance = TOTPModel.objects.filter(phone_number=phone_number).latest('created_time')
        except TOTPModel.DoesNotExist:
            raise serializers.ValidationError({"detail": "کدی برای این شماره تلفن یافت نشد."})

        if not user_otp_instance.is_valid():
            raise serializers.ValidationError({"detail": "زمان استفاده از این کد به پایان رسیده است."})

        if user_otp_instance.otp != otp_code:
            raise serializers.ValidationError({"detail": "کد ارسال شده اشتباه وارد شده است."})

        attrs['user_otp_instance'] = user_otp_instance
        return attrs

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        user_otp_instance = validated_data['user_otp_instance']

        try:
            with transaction.atomic():
                user_otp_instance.is_verified = True
                user_otp_instance.save()

                user, created = UserModel.objects.get_or_create(phone_number=phone_number)
                if created:
                    ProfileModel.objects.create(user=user)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return {
                    "detail": "کاربر با موفقیت وارد شد." if not created else "کاربر با موفقیت ایجاد شد.",
                    "refresh": str(refresh),
                    "access": access_token
                }
        except Exception as e:
            raise ValidationError(f"خطا در ورود یا ایجاد کاربر: {e}")
