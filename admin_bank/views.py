from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import BankModel, TransactionTypeModel
from .serializers import BankSerializer, TransactionTypeSerializer

from utils.admin_permission import IsSuperAdmin
from utils.custom_pagination import CustomPagination


class BankListCreateView(generics.ListCreateAPIView):
    queryset = BankModel.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination


class BankRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankModel.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsSuperAdmin]


class TransactionTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination

    def get_queryset(self):
        bank_id = self.request.query_params.get('bank_id')
        if bank_id:
            return TransactionTypeModel.objects.filter(bank_id=bank_id)
        return TransactionTypeModel.objects.all()

    def create(self, request, *args, **kwargs):
        bank_id = request.data.get('bank')
        if not BankModel.objects.filter(id=bank_id).exists():
            return Response({"error": "Bank not found."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class TransactionTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionTypeModel.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsSuperAdmin]
