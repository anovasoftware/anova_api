from django.contrib.messages import success
from core.api_views.core_api import AuthorizedAPIView, CoreAPIView
from django.apps import apps
from django.http import JsonResponse
import json
from django.db import models
from django.db.models import Q
from core.utilities.database_utilties import get_active_dict
from apps.base.models import Mapping


class TableAPIView(CoreAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = None
        self.model_name = None
        self.model: models.Model = None
        self.data_to_load = None
        self.accepted_type_ids = []
        self.type_id = None
        self.external_id_prefix = None

    def load_request(self, request):
        super().load_request(request)

        self.type_id = self.get_param('typeId', None, True)

        if not self.app_name:
            self.add_message('self.app_name not defined', success=False)
        if not self.model_name:
            self.add_message('self.model_name not defined', success=False)

        if not self.success:
            pass
        elif self.type_id not in self.accepted_type_ids:
            self.add_message(f'invalid typeId {self.type_id}', success=False)
        elif not self.load_json(request):
            pass
        else:
            self.model = apps.get_model(self.app_name, self.model_name)

    def load_json(self, request):
        loaded = True
        try:
            # Extract JSON data from request body
            data = json.loads(request.body.decode('utf-8'))

            # If expecting multiple records, ensure it's a list
            if not isinstance(data, list):
                data = [data]
            self.data_to_load = data

        except json.JSONDecodeError:
            loaded = False
            self.set_message('Invalid JSON format.', success=False)

        return loaded

    def _get(self, request):
        if self.success:
            try:
                model = apps.get_model(self.app_name, self.model_name)
                fields = self.get_value_list()
                query_filter = self.get_query_filter()

                queryset = model.objects.filter(**query_filter).values(*fields)

                self.data = list(queryset)  # Extract data and store in self.data
            except LookupError:
                self.add_message(f'Model {self.model_name} in app {self.app_name} not found', success=False)

    def get_value_list(self):
        return []

    def get_query_filter(self):
        # Define filtering criteria dynamically
        filters = {
            'type_id': self.type_id
        }

        # # Example: Filter based on request parameters
        # filter_params = self.request.GET  # Assuming request parameters are passed via GET
        #
        # # Map query parameters to model fields
        # field_mappings = {
        #     'name': 'name__icontains',
        #     'status': 'status',
        #     'created_after': 'created_at__gte',
        #     'created_before': 'created_at__lte',
        # }
        #
        # for param, field in field_mappings.items():
        #     if param in filter_params:
        #         filters[field] = filter_params[param]

        return filters  # This will be used in queryset.filter()

    def pre_post(self, request):
        if not self.data_to_load:
            self.set_message('no json data supplied', success=False)
        elif len(self.data_to_load) == 0:
            self.set_message('empty json file', success=True)
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
                self.set_message('must supply a field named pk', success=False)
            if 'external_id' not in record.keys():
                self.set_message('must supply a field named external_id', success=False)

            #
            # for record in self.data_to_load:
            #     missing_fields = set(record.keys()) - model_fields
            #     if missing_fields:
            #         message = f'Warning: These fields do not exist in {model.__name__}: {missing_fields}'
            #         self.set_message(message)
            #     else:
            #         self.add_message('loading record')

    def _post(self, request):
        records_created = 0
        records_updated = 0

        for record in self.data_to_load:
            mapping = self.get_mapping(record)
            pk = mapping.internal_id

            external_id = record['external_id']

            record = get_active_dict(self.model, record)
            model_obj, created = self.model.objects.update_or_create(
                pk=pk,
                defaults=record
            )

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

    def get_mapping(self, record):
        mapping: Mapping
        mapping, created = Mapping.objects.get_or_create(
            external_id=record['external_id'],
            defaults={
                'app_name': self.app_name,
                'model_name': self.model_name
            }
        )
        return mapping


class AuthorizedTableAPIView(AuthorizedAPIView, TableAPIView):
    pass