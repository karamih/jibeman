from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import TransactionModel
from .serializers import BatchTransactionModelSerializer, TransactionSerializer, TransactionDeleteSerializer

from utils.custom_pagination import CustomPagination


class TransactionBatchCreateView(generics.ListCreateAPIView):
    serializer_class = BatchTransactionModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return TransactionModel.objects.filter(source__account__profile=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({'detail': 'should not empty list.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionRetrieveView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionModel.objects.filter(source__account__profile__user=self.request.user)


class TransactionBatchUpdateView(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionModel.objects.filter(
            source__account__profile=self.request.user.profile)

    def patch(self, request, *args, **kwargs):
        instances = self.get_queryset()
        instance_mapping = {instance.id: instance for instance in instances}

        data = request.data
        print(data)
        if not isinstance(data, list):
            return Response({"detail": "دیتای ارسالی بایستی لیست باشد."}, status=status.HTTP_400_BAD_REQUEST)

        updated_instances = []
        errors = []

        for item in data:
            print(item)
            transaction_id = item.get('id')
            transaction_instance = instance_mapping.get(transaction_id)
            print(transaction_instance)

            if transaction_instance:
                serializer = self.get_serializer(transaction_instance, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_instances.append(serializer.data)
                else:
                    errors.append({transaction_id: serializer.errors})
            else:
                errors.append({transaction_id: "تراکنش یافت نشد."})

        if errors:
            return Response({"detail": "تراکنش آپدیت نشد.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"updated": updated_instances}, status=status.HTTP_200_OK)


class TransactionBatchDeleteView(generics.GenericAPIView):
    serializer_class = TransactionDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        transactions_to_delete = TransactionModel.objects.filter(id__in=ids,
                                                                 source__account__profile=request.user.profile)

        if not transactions_to_delete.exists():
            return Response({"detail": "تراکنشی برای پاک شدن یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        deleted_count, _ = transactions_to_delete.delete()

        return Response({"detail": f"{deleted_count} تراکنش حذف شد"}, status=status.HTTP_200_OK)
