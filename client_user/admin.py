from django.contrib import admin
from .models import UserModel, ProfileModel, TOTPModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['phone_number']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['phone_number']
    readonly_fields = ['user_id']


@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency_unit', 'created_time']
    search_fields = ['user__phone_number', 'currency_unit']
    list_filter = ['currency_unit']
    ordering = ['user__phone_number']
    readonly_fields = ['created_time']


@admin.register(TOTPModel)
class TotpModelAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'otp', 'is_verified', 'created_time']
    search_fields = ['phone_number']
    list_filter = ['is_verified', 'created_time']
    readonly_fields = ['created_time']
