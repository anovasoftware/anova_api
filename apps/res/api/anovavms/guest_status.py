from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AnovaVMSGuestStatusAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_EVENT

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=False,
            required_post=False,
        )
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Guest'
        self.hotel_id_field = 'reservation__hotel_id'
        self.treat_as_patch = True

    # def get_value_list(self):
    #     value_list = [
    #         'event_id',
    #         'code',
    #         'description',
    #         'event_start_date',
    #         'event_end_date'
    #     ] + super().get_value_list()
    #     return value_list
