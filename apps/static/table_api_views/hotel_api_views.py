from core.api_views.table_api_views import AuthorizedTableAPIView, parameters, context
from core.api_views.table_api_views import get_only_parameters, post_only_parameters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from django.core.exceptions import ObjectDoesNotExist
from apps.static.models import Hotel
from apps.res.models import Guest, GuestRoom, Event, HotelExtension

from constants import status_constants

context['hotel_id'] = 'A332'
context['hotel_description'] = 'MS Diamond'

parameters = parameters + [
    OpenApiParameter(
        name='hotelId',
        type=OpenApiTypes.STR,
        location='query',
        required=True,
        description='Hotel/ship code (contact Anova for details).'
    ),
    OpenApiParameter(
        name='guestId',
        type=OpenApiTypes.STR,
        location='query',
        required=False,
        description='Guest/passenger id (folio)'
    ),
]
get_only_parameters = get_only_parameters + []
post_only_parameters = post_only_parameters + []


class AuthorizedHotelAPIView(AuthorizedTableAPIView):
    PARAM_SPECS = AuthorizedTableAPIView.PARAM_SPECS + ('hotelId', )
    PARAM_OVERRIDES = {
        'hotelId': dict(required_get=True, required_post=True, )
    }


    def __init__(self):
        super().__init__()
        self.hotel = None
        self.client = None
        self.hotel_id = None
        self.hotel_id_field = 'hotel_id'
        self.hotel = None
        self.hotel_extension = None
        self.guest_id = None
        self.guest = None
        self.guest_room = None
        self.event = None
        # self.required_parameters = ['hotelId', ]

    def load_request(self, request):
        super().load_request(request)

    def load_models(self, request):
        super().load_models(request)

        try:
            self.hotel = Hotel.objects.get(pk=self.hotel_id)
            user_hotels = self.user.userHotels.filter(
                hotel_id=self.hotel_id,
                effective_status_id=status_constants.EFFECTIVE_STATUS_CURRENT
            )
            if not user_hotels.exists():
                message = f'access denied to hotel_id: {self.hotel_id}'
                self.set_message(message, http_status_id=status_constants.HTTP_ACCESS_DENIED)
            else:
                self.hotel_extension = HotelExtension.objects.filter(hotel_id=self.hotel_id).first()
                if not self.hotel_extension:
                    message = f'hotel_extension not found for hotel_id: {self.hotel_id}'
                    self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            message = f'hotel_id not found: {self.hotel_id}'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

        if self.success and self.guest_id:
            guests = Guest.objects.filter(pk=self.guest_id)
            if guests.exists():
                self.guest = Guest.objects.get(
                    reservation__hotel_id=self.hotel_id,
                    pk=self.guest_id
                )

                self.guest_room = GuestRoom.objects.filter(
                    room__hotel_id=self.hotel_id,
                    guest_id=self.guest_id,
                    arrival_date__date__lte=self.today,
                    departure_date__date__gt=self.today
                ).first()
                if not self.guest_room:
                    message = f'guest {self.guest.guest_id} is not onboard currently.'
                    self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
                if self.success:
                    self.event = Event.objects.filter(
                        hotel_id=self.hotel_id,
                        start_date__date__lte=self.today,
                        end_date__date__gt=self.today,
                    ).first()
                    if not self.event:
                        message = f'no event scheduled today.'
                        self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            else:
                message = f'guest_id not found: {self.guest_id}'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def validate(self, request):
        super().validate(request)

    def get_query_filter(self):
        filters = super().get_query_filter()

        filters[self.hotel_id_field] = self.hotel_id

        return filters  # This will be used in queryset.filter()

    def _get_record(self, request):
        record = super()._get_record(request)

        record = record | {
            'hotel_id': self.hotel_id,
        }
        return record

    def build_response(self):
        response = super().build_response()

        if self.hotel:
            hotel = self.hotel
            response['context']['hotel_id'] = hotel.hotel_id
            response['context']['hotel_description'] = hotel.description
        if self.guest:
            guest = self.guest
            person = guest.person
            response['context']['guestId'] = guest.guest_id
            response['context']['guestName'] = f'{person.last_name}/{person.first_name}'
            # response['context']['guest'] = {
            #     'guest_id': guest.guest_id,
            #     'person': {
            #         'person_id': person.person_id,
            #         'last_name': person.last_name,
            #         'first_name': person.first_name
            #     },
            # }

        return response
