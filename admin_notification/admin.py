from django.contrib import admin
from .models import NotificationModel


@admin.register(NotificationModel)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'message', 'created_time', 'expires_at')
    list_filter = ('created_time', 'expires_at')
    search_fields = ('title', 'message')
    ordering = ('-created_time',)
    readonly_fields = ('created_time',)

