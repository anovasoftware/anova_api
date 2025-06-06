from django.contrib.messages import success
from django.core.exceptions import ObjectDoesNotExist

from core.api_views.table_api_views import AuthorizedTableAPIView
from apps.static.models import Hotel
from apps.res.models import Guest

from constants import type_constants


class AuthorizedHotelAPIView(AuthorizedTableAPIView):
    def __init__(self):
        super().__init__()
        self.hotel = None
        self.client = None
        self.hotel_id = None
        self.hotel_id_field = 'hotel_id'
        self.hotel = None
        self.guest_id = None
        self.guest = None

    def load_request(self, request):
        super().load_request(request)
        self.hotel_id = self.get_param('hotelId', None, True)
        self.guest_id = self.get_param('guestId', None, False)

        if self.success:
            try:
                self.hotel = Hotel.objects.get(pk=self.hotel_id)
            except ObjectDoesNotExist as e:
                self.add_message(f'invalid hotelId: {self.hotel_id}', success=False)

        if self.guest_id:
            if Guest.objects.filter(pk=self.guest_id).exists():
                self.guest = Guest.objects.get(pk=self.guest_id)
            else:
                self.add_message(f'invalid guest_id: {self.guest_id}', success=False)

    def get_query_filter(self):
        filters = super().get_query_filter()

        filters[self.hotel_id_field] = self.hotel_id

        return filters  # This will be used in queryset.filter()

    def build_response(self):
        response = super().build_response()

        if self.hotel:
            hotel = self.hotel
            response['header']['hotel'] = {
                'hotel_id': hotel.hotel_id,
                # 'type__description': hotel.type.description,
                'description': hotel.description
            }
        if self.guest:
            guest = self.guest
            person = guest.person
            response['header']['guest'] = {
                'guest_id': guest.guest_id,
                'person': {
                    'person_id': person.person_id,
                    'last_name': person.last_name,
                    'first_name': person.first_name
                },
            }

        return response
