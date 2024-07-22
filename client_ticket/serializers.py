from rest_framework import serializers
from .models import Ticket, validate_image


class TicketSerializer(serializers.ModelSerializer):
    image1 = serializers.ImageField(validators=[validate_image], required=False)
    image2 = serializers.ImageField(validators=[validate_image], required=False)
    image3 = serializers.ImageField(validators=[validate_image], required=False)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'subject', 'description', 'image1', 'image2', 'image3', 'status',
                  'created_time', 'answer', 'answered_time']
        read_only_fields = ['id', 'user', 'status', 'created_time', 'answer', 'answered_time']
