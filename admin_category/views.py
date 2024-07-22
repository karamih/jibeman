from rest_framework import generics
from .models import DefaultCategoryModel
from .serializers import DefaultCategorySerializer

from utils.admin_permission import IsSuperAdmin


class DefaultCategoryListCreateView(generics.ListCreateAPIView):
    queryset = DefaultCategoryModel.objects.all()
    serializer_class = DefaultCategorySerializer
    permission_classes = [IsSuperAdmin]

    def perform_create(self, serializer):
        serializer.save()


class DefaultCategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DefaultCategoryModel.objects.all()
    serializer_class = DefaultCategorySerializer
    permission_classes = [IsSuperAdmin]
