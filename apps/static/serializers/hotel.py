from rest_framework import serializers
from apps.static.models import Hotel
from apps.res.serializers.event import EventSerializer

class HotelSerializer(serializers.ModelSerializer):
    current_event = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            'hotel_id',
            'type_id',
            'code',
            'description',
            'current_event'
        )

    def get_current_event(self, hotel):
        hotel_extension = hotel.hotel_extensions.first()

        result = None

        if hotel_extension:
            result = EventSerializer(hotel_extension.current_event).data

        return result