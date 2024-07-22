from django_filters import rest_framework as filters
from client_auth.models import UserModel


class UserFilter(filters.FilterSet):
    is_staff = filters.BooleanFilter(field_name='admin_user__is_staff')
    is_superuser = filters.BooleanFilter(field_name='admin_user__is_superuser')
    is_simple_user = filters.BooleanFilter(method='filter_simple_user')

    class Meta:
        model = UserModel
        fields = {
            'is_active': ['exact'],
            'is_staff': ['exact'],
            'is_superuser': ['exact']
        }

    def filter_simple_user(self, queryset, name, value):
        if value:
            return queryset.filter(admin_user__isnull=True, is_superuser=False, is_staff=False)
        return queryset
