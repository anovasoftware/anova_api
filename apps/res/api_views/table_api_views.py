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

    def load_request(self, request):
        super().load_request(request)
        self.hotel_id = self.get_param('hotelId', None, True)

        if self.success:
            try:
                hotel = Hotel.objects.get(pk=self.hotel_id)
            except ObjectDoesNotExist as e:
                self.add_message(f'invalid hotelId: {self.hotel_id}', success=False)

    def get_value_list(self):
        value_list = [
            'hotel__hotel_id',
            'hotel__description',
        ] + super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()

        filters['hotel_id'] = self.hotel_id

        # # Example: Filter based on request parameters
        # filter_params = self.request.GET  # Assuming request parameters are passed via GET
        #
        # # Map query parameters to model fields
        # field_mappings = {
        #     'name': 'name__icontains',
        #     'status': 'status',
        #     'created_after': 'created_at__gte',
        #     'created_before': 'created_at__lte',
        # }
        #
        # for param, field in field_mappings.items():
        #     if param in filter_params:
        #         filters[field] = filter_params[param]

        return filters  # This will be used in queryset.filter()
