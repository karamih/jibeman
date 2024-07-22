from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import filters as drf_filters
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .serializers import AdminTicketSerializer, AdminTicketAnswerSerializer
from .filters import TicketFilter

from client_ticket.models import Ticket
from utils.admin_permission import IsAdmin
from utils.custom_pagination import CustomPagination


class AdminTicketListView(generics.ListAPIView):
    serializer_class = AdminTicketSerializer
    permission_classes = [IsAdmin]
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_class = TicketFilter
    ordering_fields = ['created_time']
    search_fields = ['subject', 'description', 'user__phone_number']

    def get_queryset(self):
        return Ticket.objects.all()


class AdminTicketDetailView(generics.RetrieveAPIView):
    serializer_class = AdminTicketSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Ticket.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_visited:
            instance.is_visited = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnswerTicketView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({'details': 'تیکتی با این مشخصات یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)
        if not ticket.answer:
            serializer = AdminTicketAnswerSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'تیکت پاسخ داده شد.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'این تیکت قبلا پاسخ داده شده است.'}, status=status.HTTP_400_BAD_REQUEST)
