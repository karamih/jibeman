from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import CategoryModel
from .serializers import BatchCategoryModelSerializer, CategorySerializer, CategoryUpdateSerializer, \
    CategoryDeleteSerializer

from admin_category.models import DefaultCategoryModel
from admin_category.serializers import DefaultCategoryListClientSerializer
from client_account.models import AccountModel


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchCategoryModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account = get_object_or_404(AccountModel, pk=self.kwargs['account_pk'], profile__user=self.request.user)
        return CategoryModel.objects.filter(account=account)

    def create(self, request, *args, **kwargs):
        account = get_object_or_404(AccountModel, pk=self.kwargs['account_pk'], profile__user=self.request.user)
        serializer = self.get_serializer(data=request.data, many=True, context={'account': account})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account = get_object_or_404(AccountModel, pk=self.kwargs['account_pk'], profile__user=self.request.user)
        return CategoryModel.objects.filter(account=account)


class CategoryBatchUpdateView(generics.GenericAPIView):
    serializer_class = CategoryUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account = get_object_or_404(AccountModel, pk=self.kwargs['account_pk'], profile__user=self.request.user)
        return CategoryModel.objects.filter(account=account)

    def patch(self, request, *args, **kwargs):
        instances = self.get_queryset()
        instance_mapping = {instance.id: instance for instance in instances}

        data = request.data
        if not isinstance(data, list):
            return Response({"detail": "دیتای ارسالی بایستی لیست باشد."}, status=status.HTTP_400_BAD_REQUEST)

        updated_instances = []
        errors = []

        for item in data:
            category_id = item.get('id')
            category_instance = instance_mapping.get(category_id)

            if category_instance:
                serializer = self.get_serializer(category_instance, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_instances.append(serializer.data)
                else:
                    errors.append({category_id: serializer.errors})
            else:
                errors.append({category_id: "دسته بندی یافت نشد."})

        if errors:
            return Response({"detail": "دسته بندی آپدیت نشد.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"updated": updated_instances}, status=status.HTTP_200_OK)


class CategoryBatchDeleteView(generics.GenericAPIView):
    serializer_class = CategoryDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        account = get_object_or_404(AccountModel, pk=self.kwargs['account_pk'], profile__user=self.request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        categories_to_delete = CategoryModel.objects.filter(id__in=ids, account=account)

        if not categories_to_delete.exists():
            return Response({"detail": "دسته بندی برای پاک شدن یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        default_categories = categories_to_delete.filter(is_default=True)
        if default_categories.exists():
            return Response({"detail": "دسته بندی پیش فرض قابل حذف نمی باشد."}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = categories_to_delete.delete()

        return Response({"detail": f"{deleted_count} دسته بندی حذف شد"}, status=status.HTTP_200_OK)


class ListDefaultCategoryView(generics.ListAPIView):
    queryset = DefaultCategoryModel.objects.all()
    serializer_class = DefaultCategoryListClientSerializer
    permission_classes = [permissions.IsAuthenticated]
