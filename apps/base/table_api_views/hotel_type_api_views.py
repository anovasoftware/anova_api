from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView


class AuthorizedHotelTypeAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'HotelType'
        self.hotel_id_field = 'hotel_id'
        self.accepted_type_ids = ['ALL']

        # load_hotel_types()

    def get_value_list(self):
        value_list = [
            'hotel__hotel_id',
            'hotel__description',
            'type__type_id',
            'type__description',
            'item__item_id',
            'item__description',
        ] + super().get_value_list()
        return value_list


