from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedGuestAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Guest'
        self.hotel_id_field = 'reservation__hotel_id'
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
            type_constants.RES_GUEST_GUEST,
            type_constants.RES_GUEST_CREW,
            type_constants.RES_GUEST_STAFF
        ]

    def get_value_list(self):
        value_list = [
            'guest_id',
            'person__first_name'
        ] + super().get_value_list()
        return value_list
