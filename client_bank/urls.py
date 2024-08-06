from django.urls import path
from .views import BankListFilteredByUpdatedTimeView

urlpatterns = [
    path('banks', BankListFilteredByUpdatedTimeView.as_view(), name='client-bank-list-filtered'),
]
