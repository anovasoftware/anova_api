from apps.res.api_views.table_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'GuestRoom'
        self.hotel_id_field = 'guest__reservation__hotel_id'
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
        ]

    def get_value_list(self):
        value_list = [
            'guest_room_id',
            'arrival_date',
            'departure_date'
        ] + super().get_value_list()
        return value_list
