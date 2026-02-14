from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants
from apps.base.models import Person

# user profile
class AuthorizedForm004APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_004
    form_id = form_constants.PROFILE
    PARAM_SPECS = AuthorizedFormAPIView.PARAM_SPECS + ('workingUserId', )

    def __init__(self):
        super().__init__()
        self.working_user_id = None

    def load_request(self, request):
        super().load_request(request)
        print(request.data)
        params = self.get_param('params', {})
        self.working_user_id = params.get('workingUserId', None)
        print(self.working_user_id)

    def get_field_value(self, field):
        value = ''
        if False:
            pass
        # elif field.get('name') == 'string01':
        #     value = 'jwburke@gmail.com'
        # elif field.get('name') == 'string02':
        #     value = 'Mr.'
        # elif field.get('name') == 'string03':
        #     value = 'John'
        # elif field.get('name') == 'string04':
        #     value = 'W.'
        # elif field.get('name') == 'string05':
        #     value = 'Burke'
        else:
            value = super().get_field_value(field)
        return value

    def validate_post(self, request):
        super().validate_post(request)

    def post_post(self, request):
        super().post_post(request)


