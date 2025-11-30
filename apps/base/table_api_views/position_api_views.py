from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedPositionAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.BASE_POSITION

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Position'
        self.accepted_type_ids = [
            type_constants.BASE_POSITION_ONBOARD,
        ]

    def get_value_list(self):
        value_list = [
            'type_id',
            'code',
            'description'
        ] + super().get_value_list()
        return value_list

