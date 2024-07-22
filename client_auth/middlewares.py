from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import SessionModel

UserModel = get_user_model()


def get_user(token):
    try:
        jwt_token = UntypedToken(token)
        user_id = jwt_token.payload.get('user_id')
        user = UserModel.objects.get(user_id=user_id)
        return user
    except (InvalidToken, UserModel.DoesNotExist):
        return None


class JWTSessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if token:
            token = token.split()[1]
            user = get_user(token)
            if user:
                request.user = SimpleLazyObject(lambda: user)
                jwt_token = UntypedToken(token)
                session_key = jwt_token.payload.get('session_key')
                if not SessionModel.objects.filter(session_key=session_key, user=request.user).exists():
                    return JsonResponse({"detail": "نشست نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"detail": "توکن بی‌اعتبار است."}, status=status.HTTP_400_BAD_REQUEST)
        response = self.get_response(request)
        return response
