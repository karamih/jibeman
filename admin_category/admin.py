from django.contrib import admin
from .models import DefaultCategoryModel


@admin.register(DefaultCategoryModel)
class DefaultCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type', 'is_default', 'created_time', 'updated_time')
    readonly_fields = ('created_time', 'updated_time')
    list_filter = ('transaction_type', 'is_default')
    search_fields = ('name',)
    ordering = ('name', 'transaction_type')
