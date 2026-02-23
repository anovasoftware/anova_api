from apps.base.serializers.user import UserSerializer
from apps.static.serializers.client import ClientSerializer
from apps.static.serializers.hotel import HotelSerializer
from apps.static.models import Client, Hotel
from apps.base.models import UserHotel
from constants import hotel_constants


def get_user_profile(user, is_logged_in=False):
    user_id = user.user_id
    client_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel__client_id', flat=True)
    clients = Client.objects.filter(client_id__in=client_ids).order_by('description')

    hotel_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel_id', flat=True)
    hotels = Hotel.objects.filter(hotel_id__in=hotel_ids).order_by('description')

    if hotels.exists() and user.last_hotel_id == hotel_constants.NOT_APPLICABLE:
        user.last_hotel_id = hotels.first().hotel_id
        user.save()

    profile = UserSerializer(user).data
    profile['is_logged_in'] = is_logged_in
    profile['hotels'] = HotelSerializer(hotels, many=True).data
    profile['clients'] = ClientSerializer(clients, many=True).data


    return profile