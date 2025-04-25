from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedEventAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Event'
        self.hotel_id_field = 'hotel_id'
        self.accepted_type_ids = [
            type_constants.RES_EVENT_CRUISE,
            type_constants.RES_EVENT_TOUR
        ]

    def get_value_list(self):
        value_list = [
            'event_id',
            'code',
            'description',
            'event_start_date',
            'event_end_date'
        ] + super().get_value_list()
        return value_list
