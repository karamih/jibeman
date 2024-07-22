from django.contrib import admin
from .models import BudgetModel


@admin.register(BudgetModel)
class BudgetModelAdmin(admin.ModelAdmin):
    list_display = ('account', 'category', 'amount', 'remaining', 'cycle_start_date', 'cycle_end_date', 'alarm_percent')
    list_filter = ('account', 'category', 'cycle_start_date', 'cycle_end_date')
    search_fields = ('account__name', 'category__name')
    ordering = ('-cycle_start_date',)

