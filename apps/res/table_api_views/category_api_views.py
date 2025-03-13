from core.api_views.table_api_views import AuthorizedTableAPIView

from constants import type_constants


class AuthorizedCategoryAPIView(AuthorizedTableAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Category'
        self.accepted_type_ids = [
            type_constants.RES_CATEGORY_ROOM_CABIN,
        ]

    def get_value_list(self):
        value_list = [
            'code',
            'description'
        ]
        return value_list
