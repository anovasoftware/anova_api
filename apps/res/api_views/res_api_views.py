from django.contrib.messages import success
from django.core.exceptions import ObjectDoesNotExist

from core.api_views.table_api_views import AuthorizedTableAPIView
from apps.res.models import Hotel

from constants import type_constants


class AuthorizedHotelAPIView(AuthorizedTableAPIView):
    def __init__(self):
        super().__init__()
        self.hotel = None
        self.client = None
        self.hotel_id = None
        self.hotel_id_field = 'hotel_id'
        self.hotel = None

    def load_request(self, request):
        super().load_request(request)
        self.hotel_id = self.get_param('hotelId', None, True)

        if self.success:
            try:
                self.hotel = Hotel.objects.get(pk=self.hotel_id)
            except ObjectDoesNotExist as e:
                self.add_message(f'invalid hotelId: {self.hotel_id}', success=False)

    # def get_value_list(self):
    #     value_list = [
    #         'hotel__hotel_id',
    #         'hotel__description',
    #     ] + super().get_value_list()
    #     return value_list

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

        return response
