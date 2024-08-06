from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django_jalali.db import models as jmodels


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد.")]
    )
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='client_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='client_user_permissions',
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class ProfileModel(models.Model):
    UNIT_CHOICES = [
        ('Rial', 'Rial'),
        ('Toman', 'Toman'),
    ]
    user = models.OneToOneField(to=UserModel, related_name='profile', verbose_name='user', on_delete=models.CASCADE)
    currency_unit = models.CharField(max_length=5, choices=UNIT_CHOICES, default='Toman')
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.phone_number + ' profile'


class TOTPModel(models.Model):
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message="شماره تلفن باید 11 رقم و به فرمت 09xxxxxxxxx باشد.")]
    )
    otp = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$',
                                   message="کد عددی صحت شماره تلفن باید 6 رقم باشد.")])
    created_time = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'totp'
        verbose_name = 'Totp'
        verbose_name_plural = 'Totp\'s'

    def is_valid(self):
        return not self.is_verified and timezone.now() < self.created_time + timedelta(
            minutes=3)


class SessionModel(models.Model):
    user = models.OneToOneField(UserModel, related_name='session', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=30, primary_key=True)
    created_time = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
