from django.contrib import admin
from django_jalali.db import models as jmodels
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user', 'created_time', 'status', 'is_visited', 'answered_time')
    list_filter = ('status', 'created_time', 'answered_time')
    search_fields = ('subject', 'user__username', 'description', 'answer')
    readonly_fields = ('created_time', 'answered_time')

    fieldsets = (
        (None, {
            'fields': ('subject', 'description', 'user', 'status', 'is_visited')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
        ('Answer', {
            'fields': ('answer',)
        }),
        ('Timestamps', {
            'fields': ('created_time', 'answered_time')
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'answer' in form.changed_data:
            obj.answered_time = jmodels.datetime.datetime.now()
            obj.status = 'answered'
        super().save_model(request, obj, form, change)
