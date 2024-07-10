from rest_framework import generics, permissions
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from .models import AccountModel, ProfileModel
from .serializers import AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile = ProfileModel.objects.filter(user=self.request.user).first()
        if not profile:
            raise ValidationError("پروفایلی برای کاربر کنونی وجود ندارد.")

        try:
            serializer.save(profile=profile)
        except IntegrityError:
            raise ValidationError({'name': 'اکانت با این نام برای این پروفایل از قبل وجود دارد.'})

    def get_queryset(self):
        return AccountModel.objects.filter(profile__user=self.request.user)


class AccountRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AccountModel.objects.filter(profile__user=self.request.user)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({'name': 'اکانت با این نام برای این پروفایل از قبل وجود دارد.'})

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except IntegrityError:
            raise ValidationError({'detail': 'خطا در حذف حساب. لطفاً دوباره تلاش کنید.'})
