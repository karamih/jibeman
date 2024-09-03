from django.contrib import admin
from .models import AccountModel
from client_category.admin import CategoryInline


@admin.register(AccountModel)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'name', 'credit', 'is_active', 'created_time', 'updated_time']
    search_fields = ['profile__user__phone_number', 'name']
    list_filter = ['is_active']
    ordering = ['-created_time']
    readonly_fields = ['created_time', 'updated_time']

    inlines = [CategoryInline]
