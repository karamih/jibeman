from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveView, CategoryBatchUpdateView, CategoryBatchDeleteView, \
    ListDefaultCategoryView

urlpatterns = [
    path('account/<int:account_pk>/categories', CategoryListCreateView.as_view(), name='category-list-create'),
    path('account/<int:account_pk>/category/<int:pk>', CategoryRetrieveView.as_view(), name='category-retrieve'),
    path('account/<int:account_pk>/categories/update', CategoryBatchUpdateView.as_view(), name='category-update'),
    path('account/<int:account_pk>/categories/delete', CategoryBatchDeleteView.as_view(), name='category-delete'),
    path('default-categories', ListDefaultCategoryView.as_view(), name='default-categories-list')
]
