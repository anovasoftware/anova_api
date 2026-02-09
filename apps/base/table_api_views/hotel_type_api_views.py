from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants, process_constants

class AuthorizedHotelTypeAPIView(AuthorizedHotelAPIView):
    PARAM_SPECS = AuthorizedHotelAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                'ALL'
            )
        )
    }

    process_id = process_constants.BASE_COMPANY

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'HotelType'
        self.hotel_id_field = 'hotel_id'
        # self.accepted_type_ids = ['ALL']

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


