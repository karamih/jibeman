from django.contrib import admin
from .models import SubscriptionModel


@admin.register(SubscriptionModel)
class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ['plan', 'price', 'duration_month']
    search_fields = ['plan']
    list_filter = ['plan', 'duration_month']
    ordering = ['plan']
