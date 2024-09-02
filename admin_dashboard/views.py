from jdatetime import datetime
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from client_auth.models import ProfileModel
from client_account.models import AccountModel
from utils.admin_permission import IsAdmin


class RecentJoinedUsersView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        days = request.query_params.get('days', 7)
        try:
            days = int(days)
        except ValueError:
            return Response({'detail': 'Invalid number of days'}, status=status.HTTP_400_BAD_REQUEST)

        days_ago = datetime.today() - timedelta(days=days)
        users_num = ProfileModel.objects.filter(created_time__gte=days_ago).count()
        return Response({'recent_user_count': users_num}, status=status.HTTP_200_OK)


class RecentActiveUsersView(APIView):
    def get(self, request, *args, **kwargs):
        days = request.query_params.get('days', 7)
        try:
            days = int(days)
        except ValueError:
            return Response({'detail': 'Invalid number of days'}, status=status.HTTP_400_BAD_REQUEST)

        days_ago = datetime.today() - timedelta(days=days)
        users_num = AccountModel.objects.filter(updated_time__gte=days_ago).count()
        return Response({'recent_active_user_count': users_num}, status=status.HTTP_200_OK)
