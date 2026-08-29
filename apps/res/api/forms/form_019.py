from apps.base.utilities.user_utilities import get_user_travel_agency_company
from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, company_constants


class Form019APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_019
    form_id = form_constants.BOOKING

    def __init__(self):
        super().__init__()

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def get_field_value(self, field):
        if field.name == 'travel_agency_company_id':
            company = get_user_travel_agency_company(self.user_id, self.client_id)
            if company:
                value = company['company_id']
            else:
                value = company_constants.NOT_APPLICABLE
        else:
            value = super().get_field_value(field)

        return value