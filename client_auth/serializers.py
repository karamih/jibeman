import secrets
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import SessionModel, TOTPModel, ProfileModel

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


class MockSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد."
                                   )]
    )
    fcm_token = serializers.CharField(max_length=255)

    class Meta:
        model = UserModel
        fields = ['phone_number', 'fcm_token']


class OtpVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد.")]
    )
    otp = serializers.CharField(max_length=6)
    fcm_token = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)

    class Meta:
        model = TOTPModel
        fields = ['phone_number', 'otp', 'fcm_token']

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
        fcm_token = validated_data['fcm_token']

        try:
            with transaction.atomic():
                user_otp_instance.is_verified = True
                user_otp_instance.save()

                user, created = UserModel.objects.get_or_create(phone_number=phone_number)
                if created:
                    ProfileModel.objects.create(user=user)

                if fcm_token and user.fcm_token != fcm_token:
                    user.fcm_token = fcm_token
                    user.save()

                SessionModel.objects.filter(user=user).delete()

                session_key = secrets.token_hex(15)
                SessionModel.objects.create(user=user, session_key=session_key)

                refresh = RefreshToken.for_user(user)
                refresh['session_key'] = session_key
                access_token = refresh.access_token
                access_token['session_key'] = session_key

                return {
                    "detail": "کاربر با موفقیت وارد شد." if not created else "کاربر با موفقیت ایجاد شد.",
                    "refresh": str(refresh),
                    "access": str(access_token)
                }
        except Exception as e:
            raise ValidationError(f"خطا در ورود یا ایجاد کاربر: {e}")


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    fcm_token = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = RefreshToken(attrs['refresh'])
        session_key = refresh_token.payload.get('session_key')
        fcm_token = attrs.get('fcm_token')

        if session_key:
            data['access'] = str(refresh_token.access_token)
            refresh_token.access_token.payload['session_key'] = session_key

            user = UserModel.objects.get(user_id=refresh_token['user_id'])

            if fcm_token and user.fcm_token != fcm_token:
                user.fcm_token = fcm_token
                user.save()

        return data
