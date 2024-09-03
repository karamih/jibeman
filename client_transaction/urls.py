from django.urls import path
from .views import TransactionBatchCreateView, TransactionBatchUpdateView, TransactionBatchDeleteView, \
    TransactionRetrieveView

urlpatterns = [
    path('transactions', TransactionBatchCreateView.as_view(), name='transaction-batch-create'),
    path('transactions/batch-update', TransactionBatchUpdateView.as_view(), name='transaction-batch-update'),
    path('transactions/batch-delete', TransactionBatchDeleteView.as_view(), name='transaction-batch-delete'),
    path('transactions/<int:pk>', TransactionRetrieveView.as_view(), name='transaction-retrieve'),
]
