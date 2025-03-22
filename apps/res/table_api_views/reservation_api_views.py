from apps.res.api_views.table_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedReservationAPIView(AuthorizedHotelAPIView):
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
