from django.urls import path
from .views import FinancialSourceDetailView, FinancialSourceListCreateView

urlpatterns = [
    path('sources', FinancialSourceListCreateView.as_view(), name='financial-source-list-create'),
    path('sources/<int:pk>', FinancialSourceDetailView.as_view(), name='financial-source-retrieve-update-delete'),
]
