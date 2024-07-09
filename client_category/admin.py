from django.contrib import admin

from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'transaction_type', 'is_default', 'created_time', 'updated_time')
    search_fields = ('name', 'account__name')
    list_filter = ('is_default', 'transaction_type')
    readonly_fields = ('created_time', 'updated_time')
