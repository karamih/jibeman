from django.contrib import admin
from .models import TransactionModel


@admin.register(TransactionModel)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'category', 'source', 'amount', 'transaction_level', 'fee',
                    'date', 'created_time']
    search_fields = ['transaction_type', 'category__name', 'source__name', 'description']
    list_filter = ['transaction_type', 'category', 'date', 'created_time', 'transaction_level']
    ordering = ['date', 'created_time']
    readonly_fields = ['created_time']
