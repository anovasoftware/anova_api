from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedReservationAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_RESERVATION

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Reservation'
        self.accepted_type_ids = [
            type_constants.RES_RESERVATION_INTERNAL
        ]

    def get_value_list(self):
        value_list = [
            'reservation_id',
        ] + super().get_value_list()
        return value_list
