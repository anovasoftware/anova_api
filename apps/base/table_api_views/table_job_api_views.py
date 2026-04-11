from core.api_views.table_api_views import AuthorizedTableAPIView

from constants import type_constants, process_constants


class AuthorizedJobAPIView(AuthorizedTableAPIView):
    PARAM_NAMES = AuthorizedTableAPIView.PARAM_NAMES + ('typeId',)
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.NOT_APPLICABLE,
                type_constants.BASE_JOB_VMS_ETL,
            )
        )
    }

    process_id = process_constants.BASE_TABLE_JOB

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Job'
        # self.accepted_type_ids = [
        #     type_constants.NOT_APPLICABLE,
        #     type_constants.BASE_JOB_VMS_ETL,
        # ]

    def get_value_list(self):
        value_list = [
            'type_id',
            'code',
            'description'
        ] + super().get_value_list()
        return value_list

