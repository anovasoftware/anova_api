from core.api_views.table_api_views import AuthorizedTableAPIView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from django.core.exceptions import ObjectDoesNotExist
from apps.static.models import Hotel
from apps.res.models import Guest, GuestRoom, Event, HotelExtension

from constants import status_constants


class AuthorizedHotelAPIView(AuthorizedTableAPIView):
    DOC_CONTEXT = {
        # 'hotel_id': 'A332',
        'hotel_description': 'MS Diamond'
    }
    DOC_PARAMETERS = [
        OpenApiParameter(
            name='hotelId',
            type=OpenApiTypes.STR,
            location='query',
            required=False,
            description='Hotel/ship id. Required if hotelPublicKey is not supplied (contact Anova for details).'
        ),
        # OpenApiParameter(
        #     name='hotelPublicKey',
        #     type=OpenApiTypes.STR,
        #     location='query',
        #     required=False,
        #     description='Hotel/ship public key. Required if hotelId is not supplied (contact Anova for details).'
        # ),
        OpenApiParameter(
            name='guestId',
            type=OpenApiTypes.STR,
            location='query',
            required=False,
            description='Guest/passenger id (folio)'
        ),
    ]
    DOC_GET_ONLY_PARAMETERS = []
    DOC_POST_ONLY_PARAMETERS = []

    PARAM_NAMES = AuthorizedTableAPIView.PARAM_NAMES + ('hotelId', 'roomCode')
    PARAM_OVERRIDES = {
        'hotelId': dict(required_get=False, required_post=False, ),
        # 'hotelPublicKey': dict(required_get=False, required_post=False, ),
        'roomCode': dict(required_get=False, required_post=False, )
    }


    def __init__(self):
        super().__init__()
        self.hotel = None
        self.client = None
        self.hotel_id = None
        self.hotel_id_field = 'hotel_id'
        # self.hotel_public_key = None
        self.hotel_key = None
        self.hotel_extension = None
        self.guest_id = None
        self.guest = None
        self.guest_room = None
        self.event = None
        # self.required_parameters = ['hotelId', ]

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

        if self.success:
            pass
            # if bool(self.hotel_id) == bool(self.hotel_public_key):
            #     message = 'Exactly one of hotelId or hotelPublicKey must be provided.'
            #     self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            # else:
            #     self.hotel_key = self.hotel_id if self.hotel_id else self.hotel_public_key

            # if self.hotel_id and self.hotel_public_key:
            #     message = 'Only one of hotelId or hotelPublicKey is required.'
            #     self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            # if not self.hotel_id and not self.hotel_public_key:
            #     message = 'Either hotelPublicKey or hotelId is required.'
            #     self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def load_models(self, request):
        super().load_models(request)

        try:
            try:
                self.hotel = Hotel.objects.get(pk=self.hotel_id)
                # self.hotel_id = self.hotel.hotel_id
            except ObjectDoesNotExist as e:
                self.hotel = Hotel.objects.get(public_key=self.hotel_id)
                self.hotel_id = self.hotel.hotel_id
            # if self.hotel_public_key:
            #     self.hotel = Hotel.objects.get(public_key=self.hotel_public_key)
            #     self.hotel_id = self.hotel.hotel_id = self.hotel.hotel_id
            # else:
            #     self.hotel = Hotel.objects.get(pk=self.hotel_id)

            user_hotels = self.user.userHotels.filter(
                hotel_id=self.hotel_id,
                effective_status_id=status_constants.EFFECTIVE_STATUS_CURRENT
            )
            if not user_hotels.exists():
                message = f'access denied to hotel_id: {self.hotel_id}'
                self.set_message(message, http_status_id=status_constants.HTTP_ACCESS_DENIED)
            else:
                self.hotel_extension = HotelExtension.objects.filter(hotel_id=self.hotel_id).first()
                # if not self.hotel_extension:
                #     message = f'hotel_extension not found for hotel_id: {self.hotel_id}'
                #     self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            if self.hotel_id:
                message = f'hotelId not found: {self.hotel_id}'
            # else:
            #     message = f'hotelPublicKey not found: {self.hotel_public_key}'
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
                    arrival_date__lte=self.today,
                    departure_date__gt=self.today
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
            # response['context']['hotel_key'] = self.hotel_key
            response['context']['hotel_description'] = hotel.description
        if self.guest:
            guest = self.guest
            person = guest.person
            response['context']['guestId'] = guest.guest_id
            response['context']['guestName'] = f'{person.last_name}/{person.first_name}'
            response['context']['status'] = guest.status.description
            # response['context']['guest'] = {
            #     'guest_id': guest.guest_id,
            #     'person': {
            #         'person_id': person.person_id,
            #         'last_name': person.last_name,
            #         'first_name': person.first_name
            #     },
            # }

        return response
