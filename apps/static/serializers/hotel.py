from rest_framework import serializers
from apps.static.models import Hotel, Client

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = (
            'hotel_id',
            'code',
            'description'
        )
