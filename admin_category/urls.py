from django.urls import path
from .views import DefaultCategoryListCreateView, DefaultCategoryRetrieveUpdateDeleteView

urlpatterns = [
    path('default-categories', DefaultCategoryListCreateView.as_view(), name='admin-default-categories'),
    path('default-categories/<int:pk>', DefaultCategoryRetrieveUpdateDeleteView.as_view(),
         name='admin-default-categories-detail'),
]
