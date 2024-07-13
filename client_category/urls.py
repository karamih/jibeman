from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDeleteView

urlpatterns = [
    path('account/<int:account_id>/categories', CategoryListCreateView.as_view(), name='category-list-create'),

    path('account/<int:account_id>/category/<int:pk>', CategoryRetrieveUpdateDeleteView.as_view(),
         name='category-detail'),
]
