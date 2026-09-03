from django.db.models import Model

from apps.base.models import Person, ClientPerson
from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants, company_constants


class Form020APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_020
    form_id = form_constants.PERSON

    # PARAM_NAMES = AuthorizedFormAPIView.PARAM_NAMES + ('companyId',)
    # PARAM_OVERRIDES = {
    #     'companyId': dict(
    #         required_get=True,
    #         required_post=True,
    #         default=None
    #     ),
    # }

    def __init__(self):
        super().__init__()
        # self.company_id = company_constants.TO_BE_ANNOUNCED

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)
        # print(self.company_id)

    # def get_field_value(self, field):
    #     if field.name == 'company_id':
    #         value = self.company_id
    #     else:
    #         value = super().get_field_value(field)
    #
    #     return value

    def validate_post(self, request):
        super().validate_post(request)

        if self.success and self.record_id == 'new':
            email = self.record['email']
            person = Person.objects.filter(email=email).first()

            if person:
                message = f'email address already registered'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

                client_person = ClientPerson.objects.get_or_create(
                    client_id=self.client_id,
                    person_id=person.person_id,
                )
                self.record_id = person.pk
                # self.action = 'update'
