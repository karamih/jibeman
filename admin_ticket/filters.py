from django_filters import rest_framework as filters
from client_ticket.models import Ticket


class TicketFilter(filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'status': ['exact'],
            'is_visited': ['exact']
        }
