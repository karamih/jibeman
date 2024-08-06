import secrets
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from client_auth.models import SessionModel
from .models import AdminUserModel

User = get_user_model()


class AdminUserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.phone_number')

    class Meta:
        model = AdminUserModel
        fields = ['username', 'phone_number', 'is_staff', 'is_superuser', 'created_time']


class AdminUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(
        max_length=11,
        write_only=True,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد.")]
    )

    class Meta:
        model = AdminUserModel
        fields = ['phone_number', 'username', 'password', 'password2', 'is_superuser']
        extra_kwargs = {
            'is_superuser': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("رمز عبور یکسان نیست.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number')
        is_superuser = validated_data.pop('is_superuser')

        try:
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.set_password(password)
                user.save()
            else:
                if AdminUserModel.objects.filter(user=user).exists():
                    raise serializers.ValidationError("این کاربر ادمین است.")

            if is_superuser:
                admin_user = AdminUserModel.objects.create_superuser(user=user, **validated_data)
            else:
                admin_user = AdminUserModel.objects.create_user(user=user, **validated_data)

            admin_user.set_password(password)
            admin_user.save()
            return admin_user

        except IntegrityError:
            raise serializers.ValidationError("این کاربر ادمین است.")
        except Exception as e:
            raise serializers.ValidationError(str(e))


class AdminUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        admin_user = authenticate(username=username, password=password)

        if admin_user is None:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")

        if not admin_user.is_active:
            raise serializers.ValidationError("این حساب کاربری فعال نیست.")

        SessionModel.objects.filter(user=admin_user.user).delete()

        session_key = secrets.token_hex(15)
        SessionModel.objects.create(user=admin_user.user, session_key=session_key)

        refresh = RefreshToken.for_user(admin_user)
        refresh['session_key'] = session_key
        access_token = refresh.access_token
        access_token['session_key'] = session_key

        data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }

        return data


class AdminUpdateUsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=30,
        required=True,
        error_messages={
            'required': 'این نام کاربری الزامی است.',
            'blank': 'این نام کاربری نمی‌تواند خالی باشد.',
            'max_length': 'نام کاربری نباید بیشتر از 30 کاراکتر باشد.'
        }
    )

    class Meta:
        model = AdminUserModel
        fields = ['username']

    def validate(self, data):
        user = self.context['request'].user
        new_username = data.get('username')

        if 'username' not in data:
            raise serializers.ValidationError({'username': 'این نام کاربری الزامی است.'})

        if AdminUserModel.objects.filter(username=new_username).exists():
            if user.admin_user.username == new_username:
                raise serializers.ValidationError({'username': 'این نام کاربری، نام کاربری فعلی شما است.'})
            else:
                raise serializers.ValidationError({'username': 'این نام کاربری قبلا انتخاب شده است.'})
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance


class AdminUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True,
                                         error_messages={'required': 'وارد کردن رمز عبور قدیمی اجباری است.',
                                                         'blank': 'فیلد رمز عبور قدیمی نباید خالی باشد.'})
    new_password = serializers.CharField(required=True, write_only=True,
                                         error_messages={'required': 'وارد کردن رمز عبور جدید اجباری است.',
                                                         'blank': 'فیلد رمز عبور جدید نباید خالی باشد.'})
    confirm_password = serializers.CharField(required=True, write_only=True,
                                             error_messages={'required': 'وارد کردن تکرار رمز عبور جدید اجباری است.',
                                                             'blank': 'فیلد تکرار رمز عبور جدید نباید خالی باشد.'})

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not user.admin_user.check_password(old_password):
            raise serializers.ValidationError({'old password': 'رمز عبور شما اشتباه است.'})

        if new_password != confirm_password:
            raise serializers.ValidationError({'confirm password': 'رمز عبور جدید را تکرار کنید.'})

        if new_password == old_password:
            raise serializers.ValidationError({'new password': 'رمز عبور جدید باید متفاوت از رمز عبور قبلی باشد.'})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user.admin_user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
