from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants, process_constants


class AuthorizedJobRunAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.BASE_JOB_RUN

    PARAM_SPECS = AuthorizedHotelAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=True,
            allowed=(
                type_constants.NOT_APPLICABLE,
            )
        )
    }


    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'JobRun'
        # self.hotel_id_field = 'hotel_id'
        # self.accepted_type_ids = [
        #     type_constants.NOT_APPLICABLE,
        # ]

    def get_value_list(self):
        value_list = [
            'job_run_id',
        ] + super().get_value_list()
        return value_list

