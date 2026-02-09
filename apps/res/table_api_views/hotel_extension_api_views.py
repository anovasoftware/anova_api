from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedHotelExtensionAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_HOTEL_EXTENSION

    PARAM_SPECS = AuthorizedHotelAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.NOT_APPLICABLE
            )
        )
    }


    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'HotelExtension'
        # self.accepted_type_ids = [
        #     type_constants.NOT_APPLICABLE
        # ]

    def get_value_list(self):
        value_list = [
            'hotel_id',
            'current_event_id',
        ]
        return value_list
