from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDeleteView, ListDefaultCategoryView

urlpatterns = [
    path('account/<int:account_id>/categories', CategoryListCreateView.as_view(), name='category-list-create'),

    path('account/<int:account_id>/category/<int:pk>', CategoryRetrieveUpdateDeleteView.as_view(),
         name='category-detail'),
    path('default-categories', ListDefaultCategoryView.as_view(), name='default-categories-list')
]
