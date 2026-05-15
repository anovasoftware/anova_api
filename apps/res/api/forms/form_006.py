from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants
from apps.base.models import User
from apps.base.utilities.user_utilities import get_user_profile

# user profile
class Form006APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_006
    form_id = form_constants.CABIN_CONFIGURATION

    def __init__(self):
        super().__init__()

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def get_field_value(self, field):
        value = ''
        if False:
            pass
        else:
            value = super().get_field_value(field)
        return value

    def validate_post(self, request):
        super().validate_post(request)

    def pre_post(self, request):
        super().pre_post(request)

    def post_post(self, request):
        super().post_post(request)
