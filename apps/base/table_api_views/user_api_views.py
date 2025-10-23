from core.api_views.table_api_views import PublicTableAPIView
from apps.base.models import User
from constants import type_constants, status_constants
# from utilities.user_utilities import get_user_roles
# from django.db.models import Case, When, Value as V, Q
# from utilities.user_utilities import is_impersonator, is_developer
# from utilities.user_utilities import RoleManager
# from utilities.configuration_utilities import get_configuration_value
# from django.conf import settings
# from utilities.background_task_utilities import process_background_tasks
# from datetime import timedelta
# from django.utils import timezone


class PublicUserAPIView(PublicTableAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'User'
        self.type_id = '000'
        self.accepted_type_ids = [
            type_constants.NOT_APPLICABLE,
        ]

        self.user = None

    def load_request(self, request):
        super().load_request(request)

        if self.user_id:
            try:
                self.user = User.objects.filter(user_id=self.user_id)
            except Exception as e:
                message = f'room not found: {self.user_id}'
                self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
    def get_value_list(self):
        value_list = [
            'username',
        ]

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        if self.user_id:
            filters['user_id'] = self.user_id

        return filters

    def post_get(self, request):
        mask_fields = []

        # for record in self.records:
        #     for mask_field in mask_fields:
        #         if mask_field in record:
        #             record[mask_field] = mask_string(record[mask_field])

        super().post_get(request)

    def build_response(self):
        response = super().build_response()
        # response['detail']['user'] = 'hello'
        return response

