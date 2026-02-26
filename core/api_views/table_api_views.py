from core.api_views.core_api import AuthorizedAPIView, CoreAPIView, PublicAPIView, parameters, post_only_parameters
from core.utilities.api_utilities import transform_records
from core.api_views.core_api import post_only_parameters,get_only_parameters
from core.api_views.core_api import context
from django.apps import apps
import json
from django.db import models
from core.utilities.database_utilties import get_active_dict
from apps.static.models import Type
from apps.base.models import ExternalMapping
from constants import status_constants
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

# type_id_helper = 'typeId helper'

context = context
parameters = parameters + [
    OpenApiParameter(
        name='typeId',
        type=OpenApiTypes.STR,
        location='query',
        required=True,
        description=f'Type Id (contact Anova for details)',
    ),
    OpenApiParameter(
        name='postingType',
        type=OpenApiTypes.STR,
        location='query',
        required=False,
        default='batch',
        description=f'Posting type (batch or simple).',
    ),
]
post_only_parameters = post_only_parameters + ['postingType']
get_only_parameters = get_only_parameters + []


class TableAPIView(CoreAPIView):
    PARAM_SPECS = CoreAPIView.PARAM_SPECS + ('typeId', )

    def __init__(self):
        super().__init__()
        self.app_name = None
        self.model_name = None
        self.model: models.Model = None
        self.data_to_load = None
        self.accepted_type_ids = []
        # self.accepted_status_ids = []
        self.type_id = None
        self.status_id = None
        self.type = None
        self.external_id_required = True
        self.external_id_prefix = None
        self.action = None
        self.records = []
        self.record_id = None
        self.json_required = True
        self.posting_type = 'batch'
        self.currency_id = None

    def load_request(self, request):
        super().load_request(request)

        if not self.app_name:
            self.add_message('self.app_name not defined', http_status_id='VALIDATION_ERROR')
        if not self.model_name:
            self.add_message('self.model_name not defined', http_status_id=status_constants.HTTP_BAD_REQUEST)

        if not self.success:
            pass
        else:
            self.model = apps.get_model(self.app_name, self.model_name)
            try:
                self.type = Type.objects.get(type_id=self.type_id)
                context['type__description'] = self.type.description
            except Exception as e:
                pass

        if request.method == 'POST':
            self.posting_type = self.get_param('postingType', 'batch', False)

    def load_models(self, request):
        super().load_models(request)

    def validate(self, request):
        super().validate(request)

    def validate_patch(self, request):
        allowed_fields = {'pk', 'last_hotel_id'}
        required_fields = {'pk'}
        data_to_load = self.data_to_load

        for i, row in enumerate(data_to_load):
            row_fields = set(row)

            invalid_fields = row_fields - allowed_fields
            missing_fields = required_fields - row_fields

            if invalid_fields:
                message = f'Invalid fields: {", ".join(invalid_fields)}'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            if self.success and missing_fields:
                message = f'Missing required fields: {", ".join(missing_fields)}'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            if not self.success:
                break

    def _patch(self, request):
        records_updated = 0

        for record in self.data_to_load:
            pk = record['pk']
            record = get_active_dict(self.model, record)

            records_updated += self.model.objects.filter(pk=pk).update(**record)

        self.data['records_updated'] = records_updated

    def load_json(self, request):
        loaded = True
        try:
            # Extract JSON data from request body
            data = json.loads(request.body.decode('utf-8'))

            # If expecting multiple records, ensure it's a list
            if not isinstance(data, list):
                data = [data]
            self.data_to_load = data

        except json.JSONDecodeError as e:
            loaded = False
            if self.json_required:
                message = f'invalid JSON format in request body: {str(e)}'
                self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

        return loaded

    def pre_get(self, request):
        super().pre_get(request)
        if self.success:
            fields = self.get_value_list()
            if len(fields) == 0:
                message = f'no fields specified for {self.model_name}'
                self.add_message(message, http_status_id=status_constants.HTTP_METHOD_NOT_ALLOWED)

    def _get(self, request):
        if self.success:
            try:
                model = apps.get_model(self.app_name, self.model_name)
                fields = self.get_value_list()
                query_filter = self.get_query_filter()
                queryset = model.objects.filter(**query_filter).values(*fields)
                self.records = list(queryset)
            except LookupError:
                message = f'Model {self.model_name} in app {self.app_name} not found'
                self.add_message(message, http_status_id='VALIDATION_ERROR')

    def get_value_list(self):
        return []
        # return [
        #     'type__type_id',
        #     'type__description'
        # ]

    def get_query_filter(self):
        filters = {}
        if self.type:
            # type_ids = [self.type_id, type_constants.NOT_APPLICABLE]
            type_ids = [self.type_id, ]
            filters = {
                'type_id__in': type_ids
            }
        return filters

    def post_get(self, request):
        self.records = transform_records(self.records, shape=self.result_shape)

    def pre_post(self, request):
        if not self.load_json(request):
            pass
        elif not self.data_to_load:
            self.set_message('no json data supplied', http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif len(self.data_to_load) == 0:
            self.set_message('empty json file', http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif self.expand_record_with_internal_ids() and not self.success:
            pass
            # message = 'missing foreign key mapping(s)'
            # self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        else:
            model = self.model
            model_fields = {field.name for field in model._meta.get_fields() if isinstance(field, models.Field)}
            model_fields.add('pk')
            foreign_keys = {
                field.name: field for field in model._meta.get_fields() if isinstance(field, models.ForeignKey)
            }
            foreign_key_map = {f'{fk_field}_id': fk_field for fk_field in foreign_keys}
            model_fields.update(foreign_key_map.keys())

            record = self.data_to_load[0]
            missing_fields = set(record.keys()) - model_fields
            # if missing_fields:
            #     message = f'Warning: These fields do not exist in {model.__name__}: {missing_fields}'
            #     self.set_message(message, success=False)
            if 'pk' not in record.keys():
                message = 'must supply a field named pk'
                self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            if self.external_id_required and 'external_id' not in record.keys():
                message = 'must supply a field named external_id'
                self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def _post(self, request):
        if not self.posting_type:
            pass
        elif self.posting_type == 'batch':
            self._post_batch(request)
        elif self.posting_type == 'simple':
            self._post_simple(request)

    def _post_batch(self, request):
        records_created = 0
        records_updated = 0

        for record in self.data_to_load:
            mapping = self.get_external_mapping(record)

            pk = mapping.internal_id
            if pk == '41012':
                print('mapping')
            external_id = record['external_id']

            record = get_active_dict(self.model, record)
            model_obj, created = self.model.objects.update_or_create(
                pk=pk,
                defaults=record
            )
            if external_id == 'VMS-1401-CB-41012':
                print(f'{external_id} processed')

            # model_obj, created = self.model.objects.update_or_create(
            #     external_id=external_id,
            #     defaults=record
            # )
            if mapping.internal_id != model_obj.pk:
                mapping.internal_id = model_obj.pk
                mapping.save()

            if created:
                records_updated += 1
            else:
                records_updated += 1

        self.data['records_created'] = records_created
        self.data['records_updated'] = records_updated
        # self.set_message('under construction', success=False)

    def _get_record(self, request):
        record = {
            'user_id': self.user_id,
        }
        if self.currency_id:
            record['currency_id'] = self.currency_id

        return record

    def _post_simple(self, request):
        self.add_message('_post_simple not defined', http_status_id='SERVER_ERROR')

    def get_external_mapping(self, record):
        mapping: ExternalMapping
        mapping, created = ExternalMapping.objects.get_or_create(
            external_id=record['external_id'],
            defaults={
                'app_name': self.app_name,
                'model_name': self.model_name
            }
        )
        return mapping

    def expand_record_with_internal_ids(self):
        for record in self.data_to_load:
            for field, external_id in list(record.items()):
                if field.endswith('_external_id'):
                    model_prefix = field.replace('_external_id', '')
                    model_prefix = f'{model_prefix}'
                    pk = record['pk']
                    if pk == '41012':
                        print(pk)
                    try:
                        internal_id = ExternalMapping.objects.get(external_id=external_id).internal_id
                    except ExternalMapping.DoesNotExist:
                        message = f'{field}: internal_id not found for external_id={external_id}, pk={pk}'
                        self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
                        internal_id = None  # or handle the missing case however you like
                    record[f'{model_prefix}_id'] = internal_id
                if not self.success:
                    break
            if not self.success:
                break

        return True

    def pre_patch(self, request):
        if not self.load_json(request):
            pass

    def build_response(self):
        response = super().build_response()
        record_count = len(self.records)
        response['data']['record_count'] = record_count

        if self.type:
            response['context']['typeId'] = self.type.type_id
            response['context']['typeDescription'] = self.type.description

        # if self.type:
        #     response['context']['type__description'] = {
        #         'type_id': self.type.type_id,
        #         'code': self.type.code,
        #         'description': self.type.description
        #     }
        # response['data']['valid'] = record_count > 0
        response['data']['records'] = self.records

        return response

    # def set_status_id(self, default_value=None, required=False):
    #     status_id = self.get_param('statusId', default_value=default_value, required=required)
    #
    #     if self.success and status_id not in self.accepted_status_ids:
    #         message = f'invalid statusId {status_id}.'
    #         valid_statuses = ''
    #         for status_id in self.accepted_status_ids:
    #             valid_statuses += f', {status_id}'
    #         valid_statuses = valid_statuses[2:]
    #         message += f'{message} valid types: {valid_statuses}'
    #         self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def load_status(self, status_id):
        pass

    def add_external_mapping_to_records(self, field_name, from_field_name, app_name, model_name, records):
        unique_ids = {record.get(from_field_name) for record in records if record.get(from_field_name)}

        mappings = ExternalMapping.objects.filter(
            internal_id__in=unique_ids,
            app_name=app_name,
            model_name=model_name
        ).values_list(
            'internal_id',
            'external_id'
        )
        mappings = {
            internal_id: {
                'external_id_root': external_id,
                'external_id': external_id.rsplit('-', 1)[-1] if external_id else None,
            }
            for internal_id, external_id in mappings
        }

        for record in records:
            internal_id = record[from_field_name]

            record[field_name] = mappings[internal_id]['external_id']


class AuthorizedTableAPIView(AuthorizedAPIView, TableAPIView):
    pass


class PublicTableAPIView(PublicAPIView, TableAPIView):
    pass
