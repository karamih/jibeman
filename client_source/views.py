from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied


from .models import FinancialSourceModel
from .serializers import FinancialSourceSerializer


class FinancialSourceListCreateView(generics.ListCreateAPIView):
    serializer_class = FinancialSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.profile.user != self.request.user:
            raise PermissionDenied("شما اجازه ایجاد منبع مالی برای این حساب را ندارید.")
        serializer.save()

    def get_queryset(self):
        return FinancialSourceModel.objects.filter(account__profile__user=self.request.user)


class FinancialSourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinancialSourceModel.objects.filter(account__profile__user=self.request.user)
