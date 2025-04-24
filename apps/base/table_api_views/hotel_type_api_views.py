from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from apps.static.models import Hotel, Type
from apps.base.models import HotelType
from constants import type_constants


class AuthorizedHotelTypeAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'HotelType'
        self.hotel_id_field = 'hotel_id'
        self.accepted_type_ids = ['ALL']

        load_hotel_types()

    def get_value_list(self):
        value_list = [
            'hotel__hotel_id',
            'hotel__description',
            'type__type_id',
            'type__description',
            'item__item_id',
            'item__description',
        ] + super().get_value_list()
        return value_list


def load_hotel_types():
    hotels = Hotel.objects.filter(type_id=type_constants.HOTEL_CRUISE_SHIP)
    types = Type.objects.filter(grouping='base_hotel_type')

    existing_pairs = set(
        HotelType.objects.values_list('hotel_id', 'type_id')
    )

    new_hotel_types = []

    for hotel in hotels:
        for type in types:
            if (hotel.hotel_id, type.type_id) not in existing_pairs:
                new_hotel_types.append(
                    HotelType(hotel_id=hotel.hotel_id, type_id=type.type_id)
                )

    if new_hotel_types:
        HotelType.objects.bulk_create(new_hotel_types)