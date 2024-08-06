from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AdminUserModel
from .forms import AdminUserChangeForm, AdminUserCreationForm


@admin.register(AdminUserModel)
class AdminUserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    list_display = ('id', 'user', 'username', 'is_active', 'is_staff', 'is_superuser', 'created_time', 'updated_time')
    readonly_fields = ('id', 'created_time', 'updated_time')
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('user', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_time', 'updated_time')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'username', 'password1', 'password2', 'is_superuser'),
        }),
    )

    search_fields = ('username',)
    ordering = ('-created_time',)
    filter_horizontal = ('groups', 'user_permissions',)
