from apps.res.api_views.table_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedRoomAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Room'
        self.accepted_type_ids = [
            type_constants.RES_ROOM_CABIN,
        ]

    def get_value_list(self):
        value_list = [
            'hotel_id',
            'hotel__description',
            'type_id',
            'code',
            'description'
        ]
        return value_list
