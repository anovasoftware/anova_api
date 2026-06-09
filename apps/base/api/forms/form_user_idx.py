from apps.static.models import FormField
from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants, type_constants
from apps.base.models import UserHotel, UserRole
from apps.base.utilities.user_utilities import get_user_profile


# user/hotel profile
class FormUserIdxAPIView(AuthorizedFormAPIView):
    def __init__(self):
        super().__init__()
        self.user_idx = None
        self.user_hotels = None
        self.user_roles = None


    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

        if self.success:
            self.user_idx = self.record_id

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            self.user_hotels = UserHotel.objects.filter(
                user_id=self.user_idx
            )
        if self.success:
            self.user_idx = self.user_idx
            self.user_roles = UserRole.objects.filter(
                user_id=self.user_idx
            )


    def get_data_options(self, field):
        data_options = super().get_data_options(field)

        for data_option in data_options:
            data_option['disabled_flag'] = False

        return data_options

