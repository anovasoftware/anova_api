from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedPosMenuItemAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'PosMenuItem'
        self.accepted_type_ids = [
            type_constants.BASE_POS_MENU_ITEM_REGULAR
        ]
        self.hotel_id_field = 'pos_menu__hotel_id'

    def get_value_list(self):
        value_list = [
            'pos_menu__category__description',
            'pos_menu__currency__code',
            'pos_menu__menu_start_date',
            'pos_menu__menu_end_date',
            'price'
        ] + super().get_value_list()
        return value_list

