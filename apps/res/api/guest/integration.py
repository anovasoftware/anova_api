from django.db.models import QuerySet

from apps.res.api.guest.base import AuthorizedGuestAPIView
from apps.res.models import Guest
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from django.utils import timezone
from constants import type_constants, process_constants
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.utilities.api_docs_utilties import params_for
from core.utilities.api_docs_utilties import build_docs_response


##### CREATE ENTRY IN urls_docs.py ####
class IntegrationGuestAPIView(AuthorizedGuestAPIView):
    process_id = process_constants.INTEGRATION_GUEST
    http_method_names = ['get', 'options', 'head']

    DOC_CONTEXT = {}
    RECORD_DICT = {
        'authorized_to_charge_flag': {'description': 'Authorized to charge (Y or N).', 'example': 'Y'},
        'guest_id': {'description': 'Guest Identifier (folio number).', 'example': '0004HT'},
        'person_id': {'description': 'Internal person identifier', 'example': '0000DZ'},
        'guestRooms__room__code': {'description': 'Room/Cabin.', 'example': '302'},
        'guestRooms__arrival_date': {'description': 'Arrival date.', 'example': '2026-10-01'},
        'guestRooms__departure_date': {'description': 'Departure date.', 'example': '2026-10-12'},
        'reservation_id': {'description': 'Reservation ID. Booking reference.', 'example': '0000F8'},
        'person__last_name': {'description': 'Guest last name.', 'example': '####'},
        'person__first_name': {'description': 'Guest first name.', 'example': '##'},
        'person__salutation': {'description': 'Guest salutation.', 'example': 'MR'},
        'person__birth_date': {'description': 'Birth date (e.g., 1990-01-01).', 'example': '1955-08-20'},
        'type__code': {'description': 'Guest type.', 'example': 'Guest'},

        # 'guest__person__email': {'description': 'Guest email address.', 'example': ''},
        # 'arrival_date': {'description': 'Guest arrival date.', 'example': '2025-10-29T00:00:00Z'},
        # 'departure_date': {'description': 'Guest departure date.', 'example': '2025-11-17T00:00:00Z'},
        # 'room_id': {'description': 'Internal room/cabin identifier', 'example': '006H'},
    }
    DOC_PARAMETERS = [
        OpenApiParameter(
            name='searchString',
            type=OpenApiTypes.STR,
            location='query',
            required=True,
            description='Guest ID, room code, or guest last name.'
        ),
    ]
    DOC_PARAMETER_OVERRIDES = {
        'guestId': {'exclude': True},
    }
    DOC_GET_ONLY_PARAMETERS = []
    DOC_POST_ONLY_PARAMETERS = []
    DOC_GET_SUMMARY = 'Retrieve guest information with room/cabin/name assignment'
    DOC_GET_DESCRIPTION = 'Returns guest room/cabin info for a given room code or guest ID.'
    DOC_TAGS = ['Guest']
    DOC_EXAMPLE_NAME = 'GuestSuccess'

    PARAM_OVERRIDES = {
        **getattr(AuthorizedGuestAPIView, 'PARAM_OVERRIDES', {}),
        'searchString': dict(required_get=True)
    }

    @classmethod
    def get_schema(cls):
        parameters = cls.get_doc_parameters()
        get_only_parameters = cls.get_doc_get_only_parameters()
        post_only_parameters = cls.get_doc_post_only_parameters()
        context = cls.get_doc_context()

        _, _, response_envelope, docs_example = build_docs_response(
            record_dict=cls.RECORD_DICT,
            context=context,
            parameters=parameters,
        )

        return extend_schema_view(
            get=extend_schema(
                summary=cls.DOC_GET_SUMMARY,
                description=f'{cls.DOC_GET_DESCRIPTION}',
                tags=cls.DOC_TAGS,
                parameters=params_for(
                    method='GET',
                    parameters=parameters,
                    post_only=post_only_parameters,
                    get_only=get_only_parameters
                ),
                responses={200: response_envelope},
                examples=[
                    OpenApiExample(
                        cls.DOC_EXAMPLE_NAME,
                        value=docs_example,
                    )
                ]
            ),
            post=extend_schema(exclude=True),
        )

    def __init__(self):
        super().__init__()
        from typing import Optional, List
        self.guests: QuerySet[Guest] = Guest.objects.none()

    def load_models(self, request, *args, **kwargs):
        super().load_models(request)

        if self.success:
            hotel = self.hotel
            search_string = self.search_string
            guests = Guest.objects.filter(
                reservation__hotel_id=hotel.hotel_id,
                guest_id__iexact=search_string
            )

            if not guests.exists():
                guests = Guest.objects.filter(
                    reservation__hotel_id=hotel.hotel_id,
                    guestRooms__room__code__iexact=search_string
                )

            if not guests.exists():
                guests = Guest.objects.filter(
                    hotel_id=hotel.hotel_id,
                    person__last_name__icontains=search_string
                )

            self.guests = guests.distinct()

    def get_value_list(self):
        value_list = list(self.RECORD_DICT.keys())
        # value_list += super().get_value_list()

        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        guest_ids = self.guests.values_list('pk', flat=True)
        filters['guest_id__in'] = guest_ids

        now = timezone.now()

        filters['guestRooms__arrival_date__lte'] = now
        filters['guestRooms__departure_date__gt'] = now

        return filters

IntegrationGuestAPIView = IntegrationGuestAPIView.get_schema()(IntegrationGuestAPIView)