from django.urls import path
from .views import BankListCreateView, BankRetrieveUpdateDestroyView, TransactionTypeListCreateView, \
    TransactionTypeRetrieveUpdateDestroyView

urlpatterns = [
    path('banks', BankListCreateView.as_view(), name='list-create-bank'),
    path('banks/<int:pk>', BankRetrieveUpdateDestroyView.as_view(), name='detail-bank'),

    path('transaction-types', TransactionTypeListCreateView.as_view(), name='transaction-type-list-create'),
    path('transaction-types/<int:pk>', TransactionTypeRetrieveUpdateDestroyView.as_view(),
         name='transaction-type-detail'),
]
