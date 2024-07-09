from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PhoneNumberSerializer, OtpVerificationSerializer
from .models import UserModel, ProfileModel, TOTPModel
from .utils import generate_and_send_totp


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
            phone_number = serializer.validated_data['phone_number']
            otp_code = serializer.validated_data['otp']
            user_otp_instance = TOTPModel.objects.get(phone_number=phone_number)
            if user_otp_instance.is_valid():
                if user_otp_instance.otp == otp_code:
                    user_otp_instance.is_verified = True

                    user = UserModel.objects.create_user(phone_number=phone_number)
                    ProfileModel.objects.create(user=user)

                    return Response({"detail": "کاربر با موفقیت ایجاد شد."}, status=status.HTTP_201_CREATED)
                return Response({"detail": "کد ارسال شده اشتباه وارد شده است."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "زمان استفاده از این کد به پایان رسیده است."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
