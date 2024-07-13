from django.contrib import admin
from .models import CategoryModel


class CategoryInline(admin.TabularInline):
    model = CategoryModel
    fields = ('name', 'transaction_type', 'is_default', 'created_time', 'updated_time')
    readonly_fields = ('created_time', 'updated_time')
    list_display = ('name', 'account', 'transaction_type', 'is_default', 'created_time', 'updated_time')
    search_fields = ('name', 'account__name')
    list_filter = ('is_default', 'transaction_type')

    extra = 0

