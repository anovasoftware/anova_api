from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedItemAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Item'
        self.hotel_id_field = 'category__hotel_id'
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
            type_constants.BASE_ITEM_POINT_OF_SALE,
            type_constants.BASE_ITEM_INVENTORY,
        ]

    def get_value_list(self):
        value_list = [
            'type_id',
            'code',
            'description'
        ] + super().get_value_list()
        return value_list

