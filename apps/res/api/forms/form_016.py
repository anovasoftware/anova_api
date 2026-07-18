from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants


class Form016APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_016
    form_id = form_constants.CLIENT

    def __init__(self):
        super().__init__()

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)
        print(self.params)
