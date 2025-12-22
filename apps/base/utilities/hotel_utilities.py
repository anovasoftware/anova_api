from apps.base.models import HotelType
from apps.static.models import Hotel, Type
from constants import type_constants


def load_hotel_types():
    hotels = Hotel.objects.filter(type_id=type_constants.HOTEL_CRUISE_SHIP)
    types = Type.objects.filter(grouping='base_hotel_type')

    # existing_pairs = set(
    #     HotelType.objects.values_list('hotel_id', 'type_id')
    # )
    #
    # new_hotel_types = []

    for hotel in hotels:
        for _type in types:
            hotel_type, created = HotelType.objects.update_or_create(
                hotel_id=hotel.hotel_id,
                type_id=_type.type_id,
                defaults={'hotel': hotel, 'type': _type}
            )
            # print(f'HotelType: {hotel_type} created={created}')
            # if (hotel.hotel_id, type.type_id) not in existing_pairs:
            #     new_hotel_types.append(
            #         HotelType(hotel_id=hotel.hotel_id, type_id=type.type_id)
            #     )

    # if new_hotel_types:
    #     HotelType.objects.bulk_create(new_hotel_types)
