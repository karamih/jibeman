from django.contrib.auth.backends import BaseBackend
from ..models import AdminUserModel


class AdminUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AdminUserModel.objects.get(username=username)
            if user.check_password(password):
                return user
        except AdminUserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminUserModel.objects.get(pk=user_id)
        except AdminUserModel.DoesNotExist:
            return None
