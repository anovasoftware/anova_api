from core.api_views.core_api import AuthorizedRecordOLDAPIView
from core.api_views.table_api_views import AuthorizedRecordAPIView
from constants import type_constants, status_constants, process_constants

class ClientAPIView(AuthorizedRecordAPIView):
    process_id = process_constants.BASE_CLIENT
    PARAM_NAMES = AuthorizedRecordOLDAPIView.PARAM_NAMES
    RECORD_DICT = {
        'client_id': {'description': 'Client Id.', 'example': '221'},
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'static'
        self.model_name = 'Client'
        self.user_idx = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request)

        if self.success:
            self.user_idx = self.record_id

    def get_value_list(self):
        value_list = super().get_value_list()
        value_list += list(self.RECORD_DICT.keys())

        return value_list

    def _get(self, request):
        super()._get(request)

        if self.success and self.record:
            pass
            # first_name = self.record.get('person__first_name', '')
            # last_name = self.record.get('person__last_name', '')

