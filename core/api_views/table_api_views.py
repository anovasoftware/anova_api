from django.contrib.messages import success
from core.api_views.core_api import AuthorizedAPIView, CoreAPIView
from django.apps import apps
from django.http import JsonResponse
import json
from django.db import models
from core.utilities.database_utilties import get_active_dict


class TableAPIView(CoreAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = None
        self.model_name = None
        self.model: models.Model = None
        self.data_to_load = None
        self.accepted_type_ids = []
        self.type_id = None

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
            if missing_fields:
                message = f'Warning: These fields do not exist in {model.__name__}: {missing_fields}'
                self.set_message(message, success=False)
            elif 'pk' not in record.keys():
                self.set_message('must supply a field named pk', success=False)
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
            pk = record['pk']
            hotel_id = record['hotel_id']
            external_id = f'{self.type_id}-{hotel_id}-{pk}'

            record = get_active_dict(self.model, record)
            model_obj, created = self.model.objects.update_or_create(
                external_id=external_id,
                defaults=record
            )
            if created:
                records_updated += 1
            else:
                records_updated += 1

        self.data['records_created'] = records_created
        self.data['records_updated'] = records_updated
        # self.set_message('under construction', success=False)


class AuthorizedTableAPIView(AuthorizedAPIView, TableAPIView):
    def _get(self, request):
        if self.success:
            try:
                fields = self.get_value_list()
                model = apps.get_model(self.app_name, self.model_name)
                queryset = model.objects.all().values(*fields)

                self.data = list(queryset)  # Extract data and store in self.data
            except LookupError:
                self.add_message(f'Model {self.model_name} in app {self.app_name} not found', success=False)

    def get_value_list(self):
        return []