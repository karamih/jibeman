from django.urls import path
from .views import AdminTicketListView, AdminTicketDetailView, AnswerTicketView

urlpatterns = [
    path('tickets', AdminTicketListView.as_view(), name='admin-ticket-list'),
    path('tickets/<int:pk>', AdminTicketDetailView.as_view(), name='admin-ticket-detail'),
    path('tickets/<int:pk>/answer', AnswerTicketView.as_view(), name='admin-ticket-answer'),
]
