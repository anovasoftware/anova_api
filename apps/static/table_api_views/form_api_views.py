from core.api_views.table_api_views import PublicTableAPIView
from constants import status_constants
from apps.static.models import FormField
from core.utilities.database_utilties import get_active_dict
from core.utilities.api_utilities import get_client_ip
from django.db import models
from django.utils import timezone


class PublicFormAPIView(PublicTableAPIView):
    form_id = None
    base_model = None

    def __init__(self):
        super().__init__()
        self.record = {}
        self.app_name = 'static'
        self.model_name = 'Form'
        self.type_id = 'ALL'
        self.external_id_required = False
        self.form = None
        self.form_fields = {}
        self.accepted_type_ids = [
            'ALL'
        ]
        self.client_ip = '000.000.000.000'

        self.user = None

    def load_request(self, request):
        super().load_request(request)
        self.form_id = self.get_param('form_id', self.form_id, required=False)

        if not self.form_id:
            self.add_message(f'form_id is not defined.', success=True)
        if not self.base_model:
            self.add_message(f'base_model is not defined.', success=True)

        if self.success:
            self.client_ip = get_client_ip(request)

    def get_value_list(self):
        value_list = [
            'form_id',
            'type_id',
            'description',
            'header',
            'save_button_label',
            'save_button_action',
        ]

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['status_id'] = status_constants.ACTIVE

        if self.form_id:
            filters['form_id'] = self.form_id

        return filters

    def _get(self, request):
        super()._get(request)

        if self.success:
            self.load_form_fields()

    def load_form_fields(self):
        form_fields = FormField.objects.filter(
            form_id = self.form_id,
            status_id = status_constants.ACTIVE
        ).values(
            'form_field_id',
            'type_id',
            'control_type',
            'type__description',
            'name',
            'label',
            'default_value'
        ).order_by(
            'order_by'
        )
        self.form_fields = list(form_fields)

    def post_get(self, request):
        mask_fields = []
        if self.form_id and len(self.records) == 0:
            self.set_message(f'form_id={self.form_id} not defined.', success=False)
        else:
            self.form = self.records[0].copy()
            # self.form['form_fields'] = self.form_fields
            enriched_fields = [self.enrich_form_field(f) for f in self.form_fields]
            self.form['form_fields'] = enriched_fields

        super().post_get(request)

    def enrich_form_field(self, field):
        return {
            **field,
            'value': self.get_field_value(field)
            # 'editable': field['control_type'] == 'TEXTBOX',
            # 'required': field['type_id'] in [602, 603],
        }

    def get_field_value(self, field):
        return field.get('default_value') or ''

    def _post(self, request):
        self.record = request.data
        print(self.record)
        self.save_record(self.base_model)
    #

    def save_record(self, model: models.Model):
        pk = self.record['pk']

        record = get_active_dict(model, self.record)

        if 'last_updated' not in self.record:
            record['last_updated'] = timezone.now()

        if 'client_ip' not in self.record:
            record['client_ip'] = self.client_ip

        record['updated_by_user_id'] = self.access_user_id

        record = get_active_dict(model, record)
        try:
            pk_name = model._meta.pk.name
            pk = None if pk == 'new' else pk

            record, created = model.objects.update_or_create(**{pk_name: pk}, defaults=record)

            pk = record.pk
            # self.data['record_id'] = self.record_id
            success = True
        except Exception as e:
            self.add_message(str(e), False)
            success = False

        self.success = success

    def build_response(self):
        response = super().build_response()

        if self.form:
            response['form'] = self.form

        return response

