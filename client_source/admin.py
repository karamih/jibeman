from django.contrib import admin

from .models import FinancialSourceModel


@admin.register(FinancialSourceModel)
class FinancialSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'account', 'is_calculate', 'is_enable', 'remain', 'created_time', 'updated_time')
    search_fields = ('name', 'type', 'account__name')
    list_filter = ('type', 'is_enable')
    readonly_fields = ('created_time', 'updated_time')
