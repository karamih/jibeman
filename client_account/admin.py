from django.contrib import admin
from .models import AccountModel


@admin.register(AccountModel)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ['profile', 'name', 'credit', 'is_active', 'created_time', 'updated_time']
    search_fields = ['profile__user__phone_number', 'name']
    list_filter = ['is_active']
    ordering = ['-created_time']
    readonly_fields = ['created_time', 'updated_time']
