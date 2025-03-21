from apps.base.api_views.table_api_views import AuthorizedClientAPIView

from constants import type_constants


class AuthorizedCompanyAPIView(AuthorizedClientAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Company'
        self.accepted_type_ids = [
            type_constants.COMPANY_TRAVEL_AGENCY
        ]

    def get_value_list(self):
        value_list = [
            'company_id',
            'description',
        ] + super().get_value_list()

        return value_list

