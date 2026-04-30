from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AnovaVMSRoleItemAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.ANOVAVMS_ROLE_ITEM

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'RoleItem'

    # def get_value_list(self):
    #     value_list = [
    #         'category__description',
    #         'currency__code',
    #         'menu_start_date',
    #         'menu_end_date',
    #     ] + super().get_value_list()
    #     return value_list
    #
