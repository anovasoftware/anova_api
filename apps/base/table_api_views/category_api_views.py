from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedCategoryAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Category'
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
            type_constants.BASE_CATEGORY_ROOM_CABIN,
            type_constants.BASE_CATEGORY_POS_MENU1,
            type_constants.BASE_CATEGORY_POS_MENU2,
        ]

    def get_value_list(self):
        value_list = [
            'type_id',
            'code',
            'description'
        ] + super().get_value_list()
        return value_list

