from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AnovaVMSFloorAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_FLOOR

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES + ('typeId',)
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.FLOOR_DECK,
            )
        )
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Floor'

    def get_value_list(self):
        value_list = [
            'deck_id',
            'description'
        ]
        return value_list
