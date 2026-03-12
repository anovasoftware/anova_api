from apps.base.models import Person, EmailQueue
from apps.static.table_api_views.form_api_views import PublicFormAPIView
from constants import form_constants, page_constants, status_constants, person_constants
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.base.serializers.user import UserSerializer
from apps.base.utilities.user_utilities import get_user_profile

# contact us form
class Form005APIView(PublicFormAPIView):
    process_id = None
    form_id = form_constants.CONTACT_US

    def __init__(self):
        super().__init__()

    def get_field_value(self, field):
        lookup_value = None
        value = ''
        name = field.get('name')

        if self.user and self.user.person.person_id != person_constants.TO_BE_ANNOUNCED:
            person: Person = self.user.person
            lookup_value = getattr(person, name, '')

        if lookup_value:
            value = lookup_value
        elif name == 'email' and self.user:
            value = self.user.email
        else:
            value = super().get_field_value(field)

        return value

    def is_readonly(self, field, value=None):
        name = field.get('name')
        readonly_fields_if_populated = ('email', 'first_name', 'last_name')

        readonly = super().is_readonly(field, value)
        if readonly:
            readonly = True
        elif name in readonly_fields_if_populated and value:
            readonly = True

        return readonly


    def _post(self, request):
        record = self.record
        record_dict = self.split_record(record)
        email = record['email']

        if record['recordId'] == 'new':
            person = Person.objects.filter(email=email).first()
            if person:
                record['recordId'] = person.person_id
            else:
                super()._post(request)

        if self.success:
            person = Person.objects.filter(email=email).first()

            if person and 'email_queue' in record_dict:
                email_queue_record = record_dict['email_queue']
                email_queue_record['recordId'] = 'new'
                email_queue_record['person_id'] = person.person_id
                email_queue_record['from_email'] = person.email
                email_queue_record['reply_to_email'] = person.email
                self.save_record(EmailQueue, email_queue_record)

