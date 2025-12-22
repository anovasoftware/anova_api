from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView, parameters, context
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from django.utils import timezone
from constants import type_constants, process_constants
from core.utilities.string_utilities import mask_string
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.static.table_api_views.hotel_api_views import post_only_parameters, get_only_parameters
from core.utilities.api_docs_utilties import override_parameters, params_for
from core.utilities.api_docs_utilties import build_docs_response

context = context or {}

record_dict = {
    'room__code': {'description': 'Room/Cabin.', 'example': '302'},
    'guest__type__code': {'description': 'Guest type.', 'example': 'Guest'},
    'guest__person__last_name': {'description': 'Guest last name.', 'example': '####'},
    'guest__person__first_name': {'description': 'Guest first name.', 'example': '##'},
    'guest__person__salutation': {'description': 'Guest salutation.', 'example': 'MR'},
    'guest__person__birth_date': {'description': 'Birth date (e.g., 1990-01-01).', 'example': '1955-08-20T00:00:00Z'},
    'guest__person__email': {'description': 'Guest email address.', 'example': ''},
    'arrival_date': {'description': 'Guest arrival date.', 'example': '2025-10-29T00:00:00Z'},
    'departure_date': {'description': 'Guest departure date.', 'example': '2025-11-17T00:00:00Z'},
    'guest__authorized_to_charge_flag': {'description': 'Authorized to charge (Y or N).', 'example': 'Y'},
    'guest__reservation_id': {'description': 'Reservation ID. Booking reference.', 'example': '0000F8'},
    'guest__guest_id': {'description': 'Guest Identifier (folio number)', 'example': '0000DY'},
    'guest__person_id': {'description': 'Internal person identifier', 'example': '0000DZ'},
    'room_id': {'description': 'Internal room/cabin identifier', 'example': '006H'},
}

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
get_only_parameters = get_only_parameters + []
post_only_parameters = post_only_parameters + ['amount', 'currencyCode', ]

record_dict, record_serializer, response_envelope, docs_example = build_docs_response(
    record_dict=record_dict,
    context=context,
    parameters=parameters,
)

# record_dict = expand_record_dict(record_dict)
# record_fields = get_record_fields(record_dict)
# record_serializer = inline_serializer(name='Record', fields=record_fields)
# response_envelope = get_docs_envelope(record_serializer)
#
# docs_example = get_docs_envelope_example(
#     context=context,
#     records=[get_docs_record_example(record_dict), ],
#     parameters=get_parameters_from_open_api_parameters(parameters),
# )


@extend_schema_view(
    get=extend_schema(
        summary='Retrieve guest information with room/cabin assignment',
        description='Returns guest room/cabin info for a given room code or guest ID.',
        tags=['Guest Room'],
        parameters=params_for(
            method='GET',
            parameters=parameters,
            post_only=post_only_parameters,
            get_only=get_only_parameters
        ),

        responses={200: response_envelope},
        examples=[
            OpenApiExample(
                'GuestRoomSuccess',
                value=docs_example,  # <-- YOUR full envelope example here
            )
        ]
    ),
    post=extend_schema(exclude=True),
)
##### CREATE ENTRY IN urls_docs.py ####
class AuthorizedGuestRoomAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_GUEST_ROOM

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

# core/utilities/api_examples.py
