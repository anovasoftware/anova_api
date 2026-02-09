from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedHotelItemAPIView(AuthorizedHotelAPIView):
    PARAM_SPECS = AuthorizedHotelAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(required_get=True, required_post=True, allowed=(type_constants.RES_HOTEL_ITEM_SPECIAL_ITEM,))
    }

    process_id = process_constants.RES_HOTEL_ITEM

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'HotelItem'
        # self.accepted_type_ids = [
        #     type_constants.RES_HOTEL_ITEM_SPECIAL_ITEM
        # ]

    def get_value_list(self):
        value_list = [
            # 'hotel__description',
            # 'type__type_id',
            # 'type__description',
            'hotel_item_id',
            'special_item_type__type_id',
            'special_item_type__description',
            'special_item_type__code',
            'special_item_type__type_key',
            'item__item_id',
            'item__description'
        ] + super().get_value_list()
        return value_list
