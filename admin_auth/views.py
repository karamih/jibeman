from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AdminUserProfileSerializer, AdminUserLoginSerializer, AdminUserRegistrationSerializer, \
    AdminUpdateUsernameSerializer, AdminUpdatePasswordSerializer
from .models import AdminUserModel
from utils.admin_permission import IsSuperAdmin, IsAdmin


class AdminUserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminUserProfileSerializer

    def get_object(self):
        return AdminUserModel.objects.get(user=self.request.user)


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


class AdminUpdateUsernameView(generics.UpdateAPIView):
    serializer_class = AdminUpdateUsernameSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user.admin_user


class AdminUpdatePasswordView(generics.UpdateAPIView):
    serializer_class = AdminUpdatePasswordSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'رمز عبور با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)
