from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django_jalali.db import models as jmodels

class AdminUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class AdminUserModel(AbstractBaseUser, PermissionsMixin):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_time = jmodels.jDateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='admin_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='admin_user_permissions', blank=True)

    objects = AdminUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'admin_user'
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return self.username
