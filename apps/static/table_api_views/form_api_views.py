from typing import Optional
from django.db.models import Model

from core.api_views.table_api_views import PublicTableAPIView
from core.utilities.api_utilities import model_to_field_dict

from apps.static.models import Form, FormField, FormExtra
from apps.base.models import Parameter

from django.utils import timezone
from django.db import models
from django.apps import apps

from core.api_views.core_api import AuthorizedAPIView, CoreAPIView, PublicAPIView
from core.utilities.api_utilities import transform_records
from core.utilities.database_utilties import get_active_dict

from constants import status_constants, type_constants


FORM_VALUES = [
    'form_id',
    'type_id',
    'description',
    'header',
    'save_button_label',
    'save_button_action',
]
FORM_FIELD_VALUES = [
    'form_field_id',
    'type_id',
    'control_type',
    'type__type_id',
    'type__description',
    'type__group1',
    'name',
    'mapping_name',
    'label',
    'default_value',
    'required_flag',
    'disabled_create',
    'disabled_update',
    'custom_flag',
]


class FormAPIView(CoreAPIView):
    process_id = None
    form_id = None

    PARAM_SPECS = PublicTableAPIView.PARAM_SPECS + ('recordId', 'action')
    PARAM_OVERRIDES = {
        'recordId': dict(
            required_get=True,
            required_post=False,
        ),
        'action': dict(
            required_get=True,
            required_post=False,
        ),

    }

    def __init__(self):
        super().__init__()

        self.base_model: Optional[Model] = None
        self.record_id = None
        self.record = {}
        self.action = None
        self.type_id = 'ALL'
        self.external_id_required = False
        self.form = None
        self.form_dict = {}
        self.form_fields = []
        self.form_extras = []

    def load_request(self, request, *args, **kwargs):
        if not self.form_id:
            self.add_message(f'form_id is not defined.', http_status_id=status_constants.HTTP_OK)
        else:
            super().load_request(request, *args, **kwargs)

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            try:
                self.form = Form.objects.get(pk=self.form_id)
                self.load_form_fields()
                self.load_form_extras()
                app_name = self.form.data_source_application
                model_name = self.form.data_source_model_name
                self.base_model = apps.get_model(app_name, model_name)
                if self.is_get():
                    self.load_record()
            except Exception as e:
                message = f'error loading form: {str(e)}.'
                self.add_message(message, http_status_id=status_constants.HTTP_INTERNAL_SERVER_ERROR)


    def load_form_fields(self):
        form_fields = FormField.objects.filter(
            form_id=self.form_id,
            status_id=status_constants.ACTIVE
        ).values(
            *FORM_FIELD_VALUES
        ).order_by(
            'order_by'
        )

        action_key = f'disabled_{self.action}'
        self.form_fields = []

        for field in form_fields:
            disabled_flag = field.get(action_key, False)
            field['readonly'] = disabled_flag
            self.form_fields.append(field)

        # self.form_fields = list(form_fields)

    def load_form_extras(self):
        form_extras = FormExtra.objects.filter(
            form_id=self.form_id,
            status_id=status_constants.ACTIVE
        ).values(
            'form_extra_id',
            'type__type_id',
            'type__description',
            'description',
            'label',
            'target_form_id',
        ).order_by(
            'order_by'
        )
        self.form_extras = list(form_extras)

    def load_record(self):
        value_fields = self.get_record_values_list()

        if self.action == 'create':
            self.record = self.new_record()
        else:
            records = self.base_model.objects.filter(pk=self.record_id)
            if records.count() == 0:
                self.add_message(f'Record not found. Id {self.record_id}', False)
            else:
                self.record = records.values(*value_fields)[0]

    def new_record(self):
        record = {}
        for form_field in self.form_fields:
            value = None
            name = form_field['name']
            dv = form_field['default_value']

            if form_field['type__group1'] == 'char':
                value = dv
            # if fc.type.group1 == 'date':
            #     value = self.date_utility.get_date(flag=dv)
            # if fc.type.group1 == 'decimal':
            #     if dv == '':
            #         value = Decimal(0)
            #     else:
            #         value = Decimal(eval(dv))

            record[name] = value

        record['pk'] = 'new'

        return record

    def get_record_values_list(self):
        value_fields = []
        for form_field in self.form_fields:
            if form_field.get('custom_flag') == 'Y':
                pass
            else:
                value_fields.append(form_field['name'])

        if 'pk' not in value_fields:
            value_fields.append('pk')
        if 'static_flag' not in value_fields:
            value_fields.append('static_flag')

        return value_fields

    def _get(self, request):
        form_dict = model_to_field_dict(self.form, FORM_VALUES)
        # form_dict['readonly'] = self.record.get('static_flag') == 'Y'
        # form_readonly = form_dict.get('readonly')
        #
        # for field in self.form_fields:
        #     field['readonly'] = field.get('readonly') or form_readonly

        enriched_fields = [self.enrich_form_field(f) for f in self.form_fields]

        form_dict['form_fields'] = transform_records(enriched_fields, self.result_shape)
        form_dict['form_extras'] = transform_records(self.form_extras, self.result_shape)

        self.form_dict = form_dict

    def enrich_form_field(self, field):
        value = self.get_field_value(field)

        enriched_field = {
            **field,
            'value': value,
            'readonly': self.is_readonly(field, value),
            # 'editable': field['control_type'] == 'TEXTBOX',
            # 'required': field['type_id'] in [602, 603],
        }

        return enriched_field

    def get_field_value(self, field):
        value = ''
        name = field.get('name')
        record = self.record
        if False:
            pass
        elif name == 'username' and self.user:
            value = self.user.username
        elif record and name in record:
            value = record[name]
        else:
            value = field.get('default_value') or ''

        return value

    def is_readonly(self, field, value):
        if field.get('readonly'):
            readonly = True
        elif self.record.get('static_flag') == 'Y':
            readonly = True
        else:
            readonly = False

        return readonly

    def pre_post(self, request):
        # self.record = request.data
        self.record = self.request_data

    def _post(self, request):
        model = self.base_model
        self.save_record(model)

    def split_record(self, record):
        record_dict = {}

        for key, value in record.items():
            if '.' not in key:
                continue

            prefix, field = key.split('.', 1)

            if prefix not in record_dict:
                record_dict[prefix] = {}

            record_dict[prefix][field] = value

        return record_dict

    def save_record(self, model: type[models.Model], record=None, set_pk=True):
        record = record or self.record
        record_id = record['recordId']
        record = get_active_dict(model, record)

        if 'last_updated' not in record:
            record['last_updated'] = timezone.now()

        if 'client_ip' not in record:
            record['client_ip'] = self.client_ip

        record['updated_by_user_id'] = self.access_user_id

        record = get_active_dict(model, record)
        try:
            pk_name = model._meta.pk.name
            record_id = None if record_id == 'new' else record_id

            record, created = model.objects.update_or_create(**{pk_name: record_id}, defaults=record)

            if set_pk:
                self.record_id = record.pk
                self.data['record_id'] = self.record_id
        except Exception as e:
            self.add_message(f'error saving record: {str(e)}.', http_status_id='BAD_REQUEST')

    def build_response(self):
        response = super().build_response()

        if self.form:
            response['data']['form'] = self.form_dict

        return response


class PublicFormAPIView(PublicAPIView, FormAPIView):
    pass


class AuthorizedFormAPIView(AuthorizedAPIView, FormAPIView):
    pass


class FormParameterAPIView(PublicFormAPIView):
    PARAM_SPECS = PublicFormAPIView.PARAM_SPECS
    base_model = Parameter

    def __init__(self):
        super().__init__()

        self.parameters = {}

    # def load_request(self, request):
    #     super().load_request(request)
    #
    # def load_models(self, request):
    #     super().load_models(request)

    def pre_post(self, request):
        self.build_record(request)

    def build_record(self, request):
        record = request.data

        for field in self.form_fields:
            name = field['name']
            mapping_name = field['mapping_name']
            value = record[name]
            self.parameters[mapping_name] = record[name]
            if field['control_type'] == 'password':
                record[name] = '#' * len(value)

        self.record = record
