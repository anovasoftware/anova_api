from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from django.utils import timezone
from constants import type_constants, status_constants
from apps.res.models import Room
from core.utilities.string_utilities import mask_string


class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'GuestRoom'
        self.hotel_id_field = 'guest__reservation__hotel_id'

        self.search_options = {
            'roomCode': None,
            'lastName': None,
            'guestId': None
        }

        # self.room_code = None
        # self.last_name = None
        # self.guest_id = None
        self.room = None
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
        ]

    def load_request(self, request):
        super().load_request(request)
        # self.room_code = self.get_param('roomCode', None, False)
        # self.last_name = self.get_param('lastName', None, False)

        for option in self.search_options.keys():
            self.search_options[option] = self.get_param(option, None, False)

        # if self.room_code:
        #     try:
        #         self.room = Room.objects.get(
        #             hotel_id=self.hotel_id,
        #             code=self.room_code
        #         )
        #     except Exception as e:
        #         message = f'room not found: {self.room_code}'
        #         self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def get_value_list(self):
        value_list = [
            'room__code',
            'guest__type__code',
            'guest__person__last_name',
            'guest__person__first_name',
            'guest__person__salutation',
            'guest__person__birth_date',
            'guest__person__email',
            'arrival_date',
            'departure_date',
            'guest__authorized_to_charge_flag',

            'guest__reservation_id',
            'guest__guest_id',
            'guest__person_id',
            'room_id',


            # 'room__hotel__hotel_id',
            # 'room__hotel__description',
            # 'room__category__code',
        ]
        if self.room:
            pass

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()

        now = timezone.now()

        filters['arrival_date__lte'] = now
        filters['departure_date__gt'] = now

        room_code = self.search_options['roomCode']
        last_name = self.search_options['lastName']
        guest_id = self.search_options['guestId']
        # if my_model.arrival_date <= now <= my_model.departure_date:

        if room_code:
            filters['room__code'] = room_code

        if last_name:
            filters['guest__person__last_name__iexact'] = last_name

        if guest_id:
            filters['guest__guest_id'] = guest_id
        return filters

    def post_get(self, request):
        mask_fields = []
        # mask_fields = [
        #     'guest__person__first_name',
        #     'guest__person__last_name',
        # ]

        for record in self.records:
            for mask_field in mask_fields:
                if mask_field in record:
                    record[mask_field] = mask_string(record[mask_field])

        super().post_get(request)

    def build_response(self):
        response = super().build_response()

        # if self.room:
        #     response['context']['room'] = {
        #         'code': self.room.code
        #     }

        return response


    # def post_get(self, request):
    #     super().post_get(request)

# class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
#     pass
