from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants


class Form011APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_011
    form_id = form_constants.HOTEL

    def __init__(self):
        super().__init__()
        self.key_field = 'hotel_id'


    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)
    #
    # def get_field_value(self, field):
    #     value = ''
    #     if False:
    #         pass
    #     else:
    #         value = super().get_field_value(field)
    #     return value
    #
    # def validate_post(self, request):
    #     super().validate_post(request)
    #
    # def pre_post(self, request):
    #     super().pre_post(request)
    #
    # def post_post(self, request):
    #     super().post_post(request)
