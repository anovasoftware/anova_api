from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedHotelItemAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'HotelItem'
        self.accepted_type_ids = [
            type_constants.RES_HOTEL_ITEM_SPECIAL_ITEM
        ]

    def get_value_list(self):
        value_list = [
            'hotel__description',
            'hotel_item_id',
            'type__type_id',
            'type__description',
            'special_item_type__type_id',
            'special_item_type__description',
            'item__item_id',
            'item__description'
        ] + super().get_value_list()
        return value_list
