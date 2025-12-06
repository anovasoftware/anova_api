from apps.base.api_views.table_api_views import AuthorizedClientAPIView

from constants import type_constants, process_constants


class AuthorizedPersonAPIView(AuthorizedClientAPIView):
    process_id = process_constants.BASE_PERSON

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Person'
        self.accepted_type_ids = [
            type_constants.PERSON_HOTEL_GUEST,
        ]

    def get_value_list(self):
        value_list = [
            'person_id',
            'type_id',
            'first_name',
            'last_name',
        ]
        return value_list

