from core.api_views.core_api import AuthorizedRecordOLDAPIView
from core.api_views.table_api_views import AuthorizedRecordAPIView
from constants import process_constants

# class RoleAPIView(AuthorizedTableAPIView):
#     process_id = process_constants.BASE_ROLE2
#
#     def __init__(self):
#         super().__init__()
#         self.app_name = 'base'
#         self.model_name = 'Role'

class Role2APIView(AuthorizedRecordAPIView):
    process_id = process_constants.BASE_ROLE2
    PARAM_NAMES = AuthorizedRecordOLDAPIView.PARAM_NAMES
    RECORD_DICT = {
        'role_id': {'description': 'User Id.', 'example': '000221'},
        'description': {'description': 'Description.', 'example': 'System Administrator'},
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'Role'
        self.role_id = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request)

        if self.success:
            self.role_id = self.record_id

    def get_value_list(self):
        value_list = super().get_value_list()
        value_list += list(self.RECORD_DICT.keys())

        return value_list

    def _get(self, request):
        super()._get(request)

        if self.success and self.record:
            pass

