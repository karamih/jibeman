from django.contrib import admin
from .models import BankModel, TransactionTypeModel


class TransactionTypeInline(admin.TabularInline):
    model = TransactionTypeModel
    extra = 0


@admin.register(BankModel)
class BankModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'updated_time')
    search_fields = ('name',)
    readonly_fields = ('created_time', 'updated_time')
    inlines = [TransactionTypeInline]


@admin.register(TransactionTypeModel)
class TransactionTypeModelAdmin(admin.ModelAdmin):
    list_display = ('bank', 'type_id', 'type_name', 'type_identity')
    search_fields = ('type_name', 'type_identity')
    list_filter = ('bank',)
