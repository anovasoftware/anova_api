from django.contrib.messages import success
from core.api_views.core_api import AuthorizedAPIView, CoreAPIView, transform_records, PublicAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.apps import apps
from django.http import JsonResponse
import json
from django.db import models
from django.db.models import Q
from core.utilities.database_utilties import get_active_dict
from apps.static.models import Type
from apps.base.models import ExternalMapping
from constants import type_constants, status_constants


class TableAPIView(CoreAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = None
        self.model_name = None
        self.model: models.Model = None
        self.data_to_load = None
        self.accepted_type_ids = []
        self.type_id = None
        self.type = None
        self.external_id_required = True
        self.external_id_prefix = None
        self.records = []
        self.json_required = True
        self.posting_type = 'batch'

    def load_request(self, request):
        super().load_request(request)

        if not self.type_id:
            self.type_id = self.get_param('typeId', None, True)

        if not self.app_name:
            self.add_message('self.app_name not defined', http_status_id='VALIDATION_ERROR')
        if not self.model_name:
            self.add_message('self.model_name not defined', http_status_id=status_constants.HTTP_BAD_REQUEST)

        if not self.success:
            pass
        elif self.type_id not in self.accepted_type_ids and 'ALL' not in self.accepted_type_ids:
            message = f'invalid typeId {self.type_id}.'
            valid_types = ''

            for type_id in self.accepted_type_ids:
                valid_types += f', {type_id}'
            valid_types = valid_types[2:]
            message += f'{message} valid types: {valid_types}'
            self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        else:
            self.model = apps.get_model(self.app_name, self.model_name)
            try:
                self.type = Type.objects.get(type_id=self.type_id)
            except Exception as e:
                pass

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
                self.set_message(message, http_status_id='VALIDATION_ERROR')

        return loaded

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
        # self.data['record_count'] = len(self.records)
        # self.data['records'] = expanded_records

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
                self.set_message('must supply a field named pk', http_status_id='VALIDATION_ERROR')
            if self.external_id_required and 'external_id' not in record.keys():
                self.set_message('must supply a field named external_id', http_status_id='VALIDATION_ERROR')

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

    def build_response(self):
        response = super().build_response()

        response['meta']['record_count'] = len(self.records)
        # if self.type:
        #     response['context']['type'] = {
        #         'type_id': self.type.type_id,
        #         'code': self.type.code,
        #         'description': self.type.description
        #     }
        response['data']['records'] = self.records

        return response


class AuthorizedTableAPIView(AuthorizedAPIView, TableAPIView):
    pass


class PublicTableAPIView(PublicAPIView, TableAPIView):
    pass