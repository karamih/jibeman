from rest_framework import permissions
from admin_auth.models import AdminUserModel


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            admin_user = AdminUserModel.objects.get(user=request.user)
            return admin_user.is_superuser
        except AdminUserModel.DoesNotExist:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            admin_user = AdminUserModel.objects.get(user=request.user)
            return admin_user.is_superuser or admin_user.is_staff
        except AdminUserModel.DoesNotExist:
            return False
