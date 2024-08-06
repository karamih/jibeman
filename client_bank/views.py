from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BankFilter
from .serializers import BankWithTransactionsSerializer
from rest_framework.permissions import IsAuthenticated
from admin_bank.models import BankModel


class BankListFilteredByUpdatedTimeView(generics.ListAPIView):
    queryset = BankModel.objects.all()
    serializer_class = BankWithTransactionsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BankFilter
