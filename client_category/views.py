from rest_framework import generics, permissions
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .models import CategoryModel, AccountModel
from .serializers import CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        account = AccountModel.objects.filter(id=account_id, profile__user=self.request.user).first()
        if not account:
            raise ValidationError("این حساب متعلق به شما نیست.")
        return CategoryModel.objects.filter(account_id=account_id)

    def perform_create(self, serializer):
        account_id = self.kwargs['account_id']
        account = AccountModel.objects.filter(id=account_id, profile__user=self.request.user).first()
        if not account:
            raise ValidationError("این حساب متعلق به شما نیست.")
        serializer.save(account=account)


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        account = AccountModel.objects.filter(id=account_id, profile__user=self.request.user).first()
        if not account:
            raise ValidationError("این حساب متعلق به شما نیست.")
        return CategoryModel.objects.filter(account_id=account_id)

    def get_object(self):
        account_id = self.kwargs['account_id']
        category_id = self.kwargs['pk']
        category = CategoryModel.objects.filter(id=category_id, account_id=account_id,
                                                account__profile__user=self.request.user).first()
        if not category:
            raise ValidationError("دسته بندی مورد نظر یافت نشد یا به شما تعلق ندارد.")
        return category

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_default:
            return Response({"detail": "دسته بندی پیش فرض قابل حذف نمی باشد."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
