from django.urls import path
from .views import AccountListCreateView, AccountRetrieveUpdateDeleteView

urlpatterns = [
    path('accounts', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>', AccountRetrieveUpdateDeleteView.as_view(), name='account-retrieve-update-delete'),
]
