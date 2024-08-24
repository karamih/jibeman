import secrets
import logging
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import PhoneNumberSerializer, OtpVerificationSerializer, CustomTokenRefreshSerializer, \
    UserProfileDateSerializer, MockSerializer
from utils.otp import generate_and_send_totp
from .models import UserModel, ProfileModel, SessionModel


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


class UserProfileDataView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return ProfileModel.objects.get(user=self.request.user)


class MockAuthentication(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MockSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    phone_number = serializer.validated_data['phone_number']
                    fcm_token = serializer.validated_data['fcm_token']
                    user, created = UserModel.objects.get_or_create(phone_number=phone_number)
                    if created:
                        ProfileModel.objects.create(user=user)

                    if fcm_token and user.fcm_token != fcm_token:
                        user.fcm_token = fcm_token
                        user.save()

                    logging.info(f"Deleting tokens for user: {user}")

                    logging.info(f"Tokens deleted for user: {user}")

                    SessionModel.objects.filter(user=user).delete()

                    session_key = secrets.token_hex(15)
                    SessionModel.objects.create(user=user, session_key=session_key)

                    refresh = RefreshToken.for_user(user)
                    refresh['session_key'] = session_key
                    access_token = refresh.access_token
                    access_token['session_key'] = session_key

                    response_data = {
                        "detail": "کاربر با موفقیت وارد شد." if not created else "کاربر با موفقیت ایجاد شد.",
                        "refresh": str(refresh),
                        "access": str(access_token),
                        "phone_number": str(phone_number),
                        "currency_unit": str(user.profile.currency_unit),
                        "created_time": str(user.profile.created_time),
                        "updated_time": str(user.profile.updated_time)
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                logging.error(f"Exception during user login or creation: {e}")
                return Response('خطا در ورود یا ایجاد کاربر', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
