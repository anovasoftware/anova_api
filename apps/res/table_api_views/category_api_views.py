from apps.res.api_views.table_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedCategoryAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Category'
        self.accepted_type_ids = [
            type_constants.RES_CATEGORY_ROOM_CABIN,
        ]

    def get_value_list(self):
        value_list = [
            'hotel_id',
            'type_id',
            'code',
            'description'
        ]
        return value_list

