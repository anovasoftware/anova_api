from rest_framework import serializers
from apps.static.models import Hotel
from apps.res.models import HotelExtension
from apps.res.serializers.event import EventSerializer


class HotelExtensionSerializer(serializers.ModelSerializer):
    current_event = EventSerializer(read_only=True)

    class Meta:
        model = HotelExtension
        fields = (
            'hotel_extension_id',
            'current_event',
            'currency_id',
            # Add other extension fields here
        )


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = (
            'hotel_id',
            'type_id',
            'code',
            'description',
        )


class HotelDetailSerializer(serializers.ModelSerializer):
    # current_event = serializers.SerializerMethodField()
    hotel_extension = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            'hotel_id',
            'type_id',
            'client_id',
            'code',
            'description',
            'hotel_extension',
            # 'current_event'
        )

    # def get_current_event(self, hotel):
    #     hotel_extension = hotel.hotel_extensions.first()
    #
    #     result = None
    #
    #     if hotel_extension:
    #         result = EventSerializer(hotel_extension.current_event).data
    #
    #     return result
    def get_hotel_extension(self, hotel):
        hotel_extension = hotel.hotel_extensions.first()

        if not hotel_extension:
            return None

        return HotelExtensionSerializer(hotel_extension).data
