from apps.base.api_views.table_api_views import AuthorizedClientAPIView

from constants import type_constants, process_constants


class AuthorizedCompanyAPIView(AuthorizedClientAPIView):
    PARAM_SPECS = AuthorizedClientAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.COMPANY_TRAVEL_AGENCY
            )
        )
    }

    process_id = process_constants.BASE_COMPANY

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Company'
        # self.accepted_type_ids = [
        #     type_constants.COMPANY_TRAVEL_AGENCY
        # ]

    def get_value_list(self):
        value_list = [
            'company_id',
            'description',
        ] + super().get_value_list()

        return value_list

