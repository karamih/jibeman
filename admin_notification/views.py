from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import AdminNotificationSerializer
from utils.admin_permission import IsSuperAdmin


class AdminSendNotificationView(generics.CreateAPIView):
    serializer_class = AdminNotificationSerializer
    permission_classes = [IsSuperAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'اطلاعیه با موفقیت ارسال شد.'}, status=status.HTTP_200_OK, headers=headers)
