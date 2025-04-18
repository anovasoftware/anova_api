from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedPosMenuAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'PosMenu'
        self.accepted_type_ids = [
            type_constants.BASE_POS_MENU_MAIN
        ]

    def get_value_list(self):
        value_list = [
            'category__description',
            'currency__code',
            'menu_start_date',
            'menu_end_date',
        ] + super().get_value_list()
        return value_list

