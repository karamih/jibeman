from django.contrib import admin
from .models import TransactionModel


@admin.register(TransactionModel)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'category', 'source', 'destination', 'amount', 'transaction_level', 'fee',
                    'date', 'created_time', 'budget']
    search_fields = ['transaction_type', 'category__name', 'source__name', 'destination__name', 'description']
    list_filter = ['transaction_type', 'category', 'date', 'created_time', 'transaction_level']
    ordering = ['date', 'created_time']
    readonly_fields = ['created_time']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['transaction_type', 'amount', 'date']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            pass
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return list_filter

    def get_ordering(self, request):
        ordering = super().get_ordering(request)
        return ordering
