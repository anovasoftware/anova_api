from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView, parameters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from django.utils import timezone
from constants import type_constants
from core.utilities.string_utilities import mask_string
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.utilities.api_utilities import build_record_fields, expand_record_dict, make_envelope
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers as s

record_dict = {
    'room__code': { 'description': 'Room/Cabin.', },
    'guest__type__code': { 'description': 'Guest type.', },
    'guest__person__last_name': {'description': 'Guest last name.', },
    'guest__person__first_name': {'description': 'Guest first name.', },
    'guest__person__salutation': {'description': 'Guest salutation.', },
    'guest__person__birth_date': {
        'description': 'Birth date (e.g., 1990-01-01).',
        'type': s.DateTimeField
    },
    'guest__person__email': {'description': 'Guest email address.', },
    'arrival_date': {
        'description': 'Guest arrival date.',
        'type': s.DateTimeField
    },
    'departure_date': {
        'description': 'Guest departure date.',
        'type': s.DateTimeField
    },
    'guest__authorized_to_charge_flag': {
        'description': 'Authorized to charge (Y or N).',
    },
    'guest__reservation_id': {
        'description': 'Reservation ID. Booking reference.'
    },
    'guest__guest_id': {
        'description': 'Guest Identifier (folio number)'
    },
    'guest__person_id': {
        'description': 'Internal person identifier'
    },
    'room_id': {
        'description': 'Internal room/cabin identifier'
    },
}
record_dict = expand_record_dict(record_dict)
record_fields = build_record_fields(record_dict)
GuestRoomRecord = inline_serializer(name='GuestRoomRecord', fields=record_fields)
GuestRoomResponse = make_envelope(GuestRoomRecord)

parameters = parameters + [
    OpenApiParameter(
        name='roomCode',
        type=OpenApiTypes.STR,
        location='query',
        required=False,
        description='Room code (e.g., 101).'
    ),
    OpenApiParameter(
        name='lastName',
        type=OpenApiTypes.STR,
        location='query',
        required=False,
        description='Last name of guest (e.g., Johnson).'
    ),
]


# GuestRoomRecord = make_record_serializer('GuestRoomRecord', record_fields)
# GuestRoomEnvelope = make_envelope(GuestRoomRecord)

@extend_schema_view(
    get=extend_schema(
        summary='Retrieve guest information with room/cabin assignment',
        description='Returns guest room/cabin info for a given room code or guest ID.',
        tags=['Guest Room'],
        parameters=parameters,
        responses={200: GuestRoomResponse},
    ),
    post=extend_schema(exclude=True),
)
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

        self.room = None
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
        ]

    def load_request(self, request):
        super().load_request(request)
        for option in self.search_options.keys():
            self.search_options[option] = self.get_param(option, None, False)

    def get_value_list(self):
        value_list = list(record_dict.keys())
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

        return response
