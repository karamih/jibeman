from django_filters import rest_framework as filters
from admin_bank.models import BankModel


class BankFilter(filters.FilterSet):
    updated_after = filters.DateTimeFilter(field_name='updated_time', lookup_expr='gt')

    class Meta:
        model = BankModel
        fields = ['updated_after']
