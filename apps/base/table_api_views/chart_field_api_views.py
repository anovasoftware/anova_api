from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants


class AuthorizedChartFieldAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'ChartField'
        self.hotel_id_field = 'hotel_id'
        self.accepted_type_ids = [
            type_constants.BASE_CHART_FIELD_REVENUE,
        ]

    def load_request(self, request):
        super().load_request(request)

    def get_value_list(self):
        value_list = [
            'code',
            'description',
        ]
        value_list += super().get_value_list()
        return value_list

