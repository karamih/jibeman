from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import filters as drf_filters
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .serializers import AdminUserListSerializer, AdminUserActiveSerializer
from .filters import UserFilter
from client_auth.models import UserModel
from utils.admin_permission import IsSuperAdmin
from utils.custom_pagination import CustomPagination


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserListSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_class = UserFilter
    search_fields = ['phone_number']

    def get_queryset(self):
        return UserModel.objects.filter().order_by('user_id')


class ActivateUserView(APIView):
    permission_classes = [IsSuperAdmin]

    def patch(self, request, pk):
        try:
            user = UserModel.objects.get(user_id=pk, admin_user__is_superuser=False)
        except UserModel.DoesNotExist:
            return Response({'details': 'کاربری یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminUserActiveSerializer(user, data=request.data)
        if serializer.is_valid():
            user.is_active = serializer.validated_data['is_active']
            user.save()
            return Response({'detail': 'کاربر فعال شد.' if user.is_active else 'کاربر غیر فعال شد.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

