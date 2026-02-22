from apps.base.serializers.user import UserSerializer
from apps.static.serializers.client import ClientSerializer
from apps.static.serializers.hotel import HotelSerializer
from apps.static.models import Client, Hotel
from apps.base.models import UserHotel


def get_user_profile(user, is_logged_in=False):
    user_id = user.user_id
    profile = UserSerializer(user).data
    profile['is_logged_in'] = is_logged_in

    client_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel__client_id', flat=True)
    clients = Client.objects.filter(client_id__in=client_ids).order_by('description')

    hotel_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel_id', flat=True)
    hotels = Hotel.objects.filter(hotel_id__in=hotel_ids).order_by('description')

    profile['hotels'] = HotelSerializer(hotels, many=True).data
    profile['clients'] = ClientSerializer(clients, many=True).data

    return profile