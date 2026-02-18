# from Demos.SystemParametersInfo import new_value

from core.api_views.table_api_views import PublicTableAPIView
from core.api_views.table_api_views import TableAPIView
from apps.static.models import Form, FormField, FormExtra
from django.utils import timezone
from apps.base.models import Parameter
from core.api_views.core_api import AuthorizedAPIView, CoreAPIView, PublicAPIView, parameters, post_only_parameters
from core.utilities.api_utilities import transform_records
from django.db import models
from core.utilities.database_utilties import get_active_dict
from constants import status_constants, type_constants
from django.apps import apps


class FormAPIView(TableAPIView):
    process_id = None

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

    form_id = None
    base_app = None
    base_model = None

    def __init__(self):
        super().__init__()
        self.record = {}
        self.app_name = 'static'
        self.model_name = 'Form'
        self.type_id = 'ALL'
        self.external_id_required = False
        self.form = None
        self.form_fields = []
        self.form_extras = []
        # self.user = None
        self.record = None

    def load_request(self, request):
        print(self.record_id)
        super().load_request(request)
        # self.form_id = self.get_param('form_id', self.form_id, required=False)
        #
        # if not self.form_id:
        #     self.add_message(f'form_id is not defined.', http_status_id=status_constants.HTTP_OK)
        # if not self.base_model:
        #     self.add_message(f'base_model is not defined.', http_status_id=status_constants.HTTP_OK)

    def load_models(self, request):
        super().load_models(request)
        form = Form.objects.filter(form_id=self.form_id).first()
        self.base_app = form.data_source_application
        base_app_str = self.base_app
        base_model_str =form.data_source_model_name
        self.base_model = apps.get_model(base_app_str, base_model_str)

        self.load_form_fields()
        self.load_form_extras()
        self.load_form()
    # def load_models_get(self, request):
    #     super().load_models_get(request)
    #     form = Form.objects.filter(form_id=self.form_id).first()
    #     self.base_app = form.data_source_application
    #     base_app_str = self.base_app
    #     base_model_str =form.data_source_model_name
    #     self.base_model = apps.get_model(base_app_str, base_model_str)
    #
    #     self.load_form_fields()
    #     self.load_form_extras()
    #     self.load_form()
    #
    # def load_models_post(self, request):
    #     super().load_models_post(request)

    def load_form(self):
        value_fields = []
        for form_field in self.form_fields:
            if form_field.get('custom_flag') == 'Y':
                pass
                # self.custom[fc.name] = None
            else:
                value_fields.append(form_field['name'])

        value_fields.append('pk')
        value_fields.append('static_flag')

        # if self.django_utility.model_has_field(self.model, 'status_id'):
        #     self.value_fields.append('status_id')

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

        # if self.success:
        #     self.load_form_fields()
        #     self.load_form_extras()

    def load_form_fields(self):
        form_fields = FormField.objects.filter(
            form_id = self.form_id,
            status_id = status_constants.ACTIVE
        ).values(
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
            form_id = self.form_id,
            status_id = status_constants.ACTIVE
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

    def post_get(self, request):
        mask_fields = []
        if self.form_id and len(self.records) == 0:
            message = f'form_id={self.form_id} not defined.'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        else:
            form = self.records[0].copy()
            form['readonly'] = self.record.get('static_flag') == 'Y'

            # loop through again to update any settings based on action
            form_readonly = form.get('readonly')
            for field in self.form_fields:
                field['readonly'] = field.get('readonly') or form_readonly

            enriched_fields = [self.enrich_form_field(f) for f in self.form_fields]

            form['form_fields'] = transform_records(enriched_fields, self.result_shape)
            form['form_extras'] = transform_records(self.form_extras, self.result_shape)

            self.data['form'] = form

        super().post_get(request)

    def enrich_form_field(self, field):
        return {
            **field,
            'value': self.get_field_value(field)
            # 'editable': field['control_type'] == 'TEXTBOX',
            # 'required': field['type_id'] in [602, 603],
        }

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
            return field.get('default_value') or ''

        return value

    def pre_post(self, request):
        self.record = request.data

    def _post(self, request):
        self.save_record(self.base_model)
    #

    def save_record(self, model: models.Model):
        record_id = self.record['recordId']

        record = get_active_dict(model, self.record)

        if 'last_updated' not in self.record:
            record['last_updated'] = timezone.now()

        if 'client_ip' not in self.record:
            record['client_ip'] = self.client_ip

        record['updated_by_user_id'] = self.access_user_id

        record = get_active_dict(model, record)
        try:
            pk_name = model._meta.pk.name
            record_id = None if record_id == 'new' else record_id

            record, created = model.objects.update_or_create(**{pk_name: record_id}, defaults=record)

            self.record_id = record.pk
            self.data['record_id'] = self.record_id
        except Exception as e:
            self.add_message(f'error saving record: {str(e)}.', http_status_id='BAD_REQUEST')

    def build_response(self):
        response = super().build_response()

        if self.form:
            response['form'] = self.form

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


