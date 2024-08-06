from django.contrib import admin
from .models import DefaultCategoryModel


@admin.register(DefaultCategoryModel)
class DefaultCategoryModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'icon_name', 'transaction_type', 'icon_fg_color', 'is_default', 'created_time',
        'updated_time')
    readonly_fields = ('id', 'created_time', 'updated_time')
    list_filter = ('transaction_type', 'is_default')
    search_fields = ('name',)
    ordering = ('name', 'transaction_type')
