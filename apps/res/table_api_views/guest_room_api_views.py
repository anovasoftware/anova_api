from apps.res.api_views.table_api_views import AuthorizedHotelAPIView
from django.utils import timezone
from constants import type_constants
from collections import defaultdict


class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'GuestRoom'
        self.hotel_id_field = 'guest__reservation__hotel_id'
        self.room_code = None
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
        ]

    def load_request(self, request):
        super().load_request(request)
        self.room_code = self.get_param('roomCode', None, False)
        # self.data['guest_rooms'] = {}

    def get_value_list(self):
        value_list = [
            'guest_room_id',
            'arrival_date',
            'departure_date',

            'guest__guest_id',
            'guest__reservation_id',

            'guest__person__first_name',
            'guest__person__last_name',
            'guest__person__birth_date',
            # 'guest__person__gender_type__code',
            'guest__person__email',
            'room__code',
            # 'room__hotel__hotel_id',
            # 'room__hotel__description',
            # 'room__category__code',
        ] + super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()

        now = timezone.now()

        # if my_model.arrival_date <= now <= my_model.departure_date:

        filters['arrival_date__lte'] = now
        filters['departure_date__gt'] = now

        if self.room_code:
            filters['room__code'] = self.room_code

        return filters

    # def post_get(self, request):
    #     super().post_get(request)

# class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
#     pass
