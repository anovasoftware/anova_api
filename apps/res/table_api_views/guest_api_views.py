from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedGuestAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.TABLE_RES_GUEST

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES + ('typeId',)
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.NOT_APPLICABLE,
                type_constants.RES_GUEST_GUEST,
                type_constants.RES_GUEST_CREW
            )
        )
    }


    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Guest'
        self.hotel_id_field = 'hotel_id'

    def get_value_list(self):
        value_list = [
            'guest_id',
        ] + super().get_value_list()
        return value_list
