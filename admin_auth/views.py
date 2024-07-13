from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AdminUserRegistrationSerializer
from .serializers import AdminUserLoginSerializer
from .models import AdminUserModel
from .utils.admin_permission import IsSuperAdmin


class AdminUserRegisterView(generics.ListCreateAPIView):
    queryset = AdminUserModel.objects.all()
    serializer_class = AdminUserRegistrationSerializer
    permission_classes = [IsSuperAdmin]


class AdminUserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdminUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
