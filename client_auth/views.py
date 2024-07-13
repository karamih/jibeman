from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.validators import ValidationError
from .serializers import PhoneNumberSerializer, OtpVerificationSerializer
from .utils import generate_and_send_totp
from .models import UserModel, ProfileModel
from rest_framework_simplejwt.tokens import RefreshToken


class GenerateOtpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            is_send = generate_and_send_totp(phone_number=phone_number)
            if is_send:
                return Response({"detail": "کد با موفقیت ارسال شد."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "کد با موفقیت ارسال نشد."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MockAuthentication(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    phone_number = serializer.validated_data['phone_number']
                    user, created = UserModel.objects.get_or_create(phone_number=phone_number)
                    if created:
                        ProfileModel.objects.create(user=user)

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    response_data = {
                        "detail": "کاربر با موفقیت وارد شد." if not created else "کاربر با موفقیت ایجاد شد.",
                        "refresh": str(refresh),
                        "access": access_token
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response('خطا در ورود یا ایجاد کاربر', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
