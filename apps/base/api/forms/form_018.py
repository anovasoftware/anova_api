from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants, company_constants


class Form018APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_018
    form_id = form_constants.COMPANY_USER_AGENT

    PARAM_NAMES = AuthorizedFormAPIView.PARAM_NAMES + ('companyId',)
    PARAM_OVERRIDES = {
        'companyId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }

    def __init__(self):
        super().__init__()
        self.company_id = company_constants.TO_BE_ANNOUNCED

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)
        print(self.company_id)

    def get_field_value(self, field):
        if field.name == 'company_id':
            value = self.company_id
        else:
            value = super().get_field_value(field)

        return value

    def validate_post(self, request):
        super().validate_post(request)
    #
    # def pre_post(self, request):
    #     super().pre_post(request)
    #
    # def post_post(self, request):
    #     super().post_post(request)
