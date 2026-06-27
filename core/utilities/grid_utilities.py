import pandas as pd

from apps.base.utilities.hotel_utilities import get_hotel_extension
from apps.static.models import Grid, GridColumn
from apps.res.models import HotelExtension, Event
from constants import status_constants
from django.apps import apps
from typing import Optional
from django.db.models import Model
from core.utilities.data_transformation_utilities import snake_to_camel_list, snake_to_camel
from apps.base.utilities.person_utilities import PersonUtilities
from django.db.models import F

PERSON_NAME_TOKEN = '__PERSON-NAME'


class GridUtility(object):
    remove_filters = []
    query_filters = {}
    query_filters_exclude = {}

    def __init__(self, grid_id, params=None):
        self.grid_id = grid_id
        self.params = params or {}
        self.grid = None
        self.base_model: Optional[Model] = None
        self.columns = None
        self.rows_qs = None
        self.rows_df = None
        self.rows = None
        self.displayed_columns = None
        self.values_list = []
        self.order_by = None

        self.success = True
        self.message = 'grid loaded'

    def load_grid(self):
        self.load_params()
        if self.success:
            self.load_models()
        if self.success:
            self.grid = self.get_grid()
            self.columns = self.get_columns()

            app_name = self.grid['data_source_application']
            model_name = self.grid['data_source_model_name']
            self.base_model = apps.get_model(app_name, model_name)

        if self.success:
            self.displayed_columns = self.get_displayed_columns()
            self.values_list = self.get_values_list()
            self.order_by = self.get_order_by()
            self.rows_qs = self.get_data_qs()

            if self.success:
                self.rows_df = self.get_data_df()
                if self.success:
                    if self.grid.get('selectable', False):
                        self.rows_df['selected'] = False
                        self.displayed_columns = ['selected'] + self.displayed_columns

                        self.update_selected()

                    self.rows = self.get_rows()
                    if self.success:
                        remove_keys = [
                            'data_source_application',
                            'data_source_model_name',
                            'order_by'
                        ]

                        self.grid = {k: v for k, v in self.grid.items() if k not in remove_keys}
                        self.displayed_columns = snake_to_camel_list(self.displayed_columns, '_')
                        self.grid['displayed_columns'] = snake_to_camel_list(self.displayed_columns, '.')
                        self.grid['columns'] = self.columns
                        self.grid['rows'] = self.rows

    def load_params(self):
        pass

    def load_models(self):
        pass

    def get_grid(self):
        grid = Grid.objects.values(
            'grid_id',
            'form_id',
            'page_id',
            'description',
            'display_as',
            'title',
            'data_source_application',
            'data_source_model_name',
            'order_by',
            'can_create',
            'selectable'
        ).get(
            pk=self.grid_id
        )
        return grid

    def get_columns(self):
        columns = []

        columns_qs = GridColumn.objects.values(
            # 'grid_column_id',
            'description',
            'field',
            'label',
            'format'
        ).filter(
            grid_id=self.grid_id,
            status_id=status_constants.ACTIVE,
        ).order_by(
            'order_by'
        )

        columns_df = pd.DataFrame(list(columns_qs))
        # columns_df['expression'] = columns_df['field'].apply(resolve_field_expression)

        if not columns_df.empty:
            columns_df['data_path'] = columns_df['field'].apply(
                lambda x: snake_to_camel(x, join_with='.')
            )

            columns_df['field'] = columns_df['field'].apply(
                lambda x: snake_to_camel(x, join_with='_')
            )

            columns = columns_df.to_dict('records')
        else:
            self.message = 'no columns found'
            self.success = False

        if self.success and self.grid.get('selectable', False):
            columns.append({
                'description': 'selected',
                'field': 'selected',
                'label': 'Select',
                'format': 'checkbox',
                'data_path': 'selected',
            })

        return columns

    def get_query_filter(self):
        base_filters = {
            'status_id': status_constants.ACTIVE,
        }

        filters = {
            k: v for k, v in base_filters.items() if k not in self.remove_filters
        }

        filters.update(self.query_filters)
        return filters

    def get_query_filter_exclude(self):
        return self.query_filters_exclude

    def get_data_qs(self):
        filters = self.get_query_filter()
        filters_exclude = self.get_query_filter_exclude()
        queryset = self.base_model.objects.filter(
            **filters
        ).exclude(
            **filters_exclude
        )

        queryset = queryset.values(
            *self.values_list,
        ).order_by(
            *self.order_by
        )
        queryset = list(queryset)

        return queryset

    # def get_data_df(self):
    #     rows_df = pd.DataFrame(list(self.rows_qs))
    #     rows_df['transaction__guest__person__PERSON-NAME'] = 'fullname here'
    #     return rows_df

    def get_data_df(self):
        rows_df = pd.DataFrame(list(self.rows_qs))

        for field in self.displayed_columns:
            if isinstance(field, str) and field.endswith(PERSON_NAME_TOKEN):
                prefix = field[:-len(PERSON_NAME_TOKEN)]

                first_col = f'{prefix}__first_name'
                middle_name = f'{prefix}__middle_name'
                last_col = f'{prefix}__last_name'
                salutation_col = f'{prefix}__salutation'

                rows_df[field] = rows_df.apply(
                    lambda row: PersonUtilities.get_full_name(
                        first=row.get(first_col, ''),
                        middle=row.get(middle_name, ''),
                        last=row.get(last_col, ''),
                        salutation=row.get(salutation_col, '')
                    ),
                    axis=1
                )

        display_as_field = self.get_display_as()

        if display_as_field and display_as_field in rows_df.columns:
            rows_df['display_as'] = rows_df[display_as_field].fillna('')
        return rows_df

    def get_display_as(self):
        return self.grid.get('display_as', 'pk')

    def get_rows(self):
        rows = self.rows_df.to_dict('records')
        return rows

    def update_selected(self):
        pass

    def get_displayed_columns(self):
        columns = GridColumn.objects.filter(
            grid_id=self.grid_id,
            status_id=status_constants.ACTIVE,
        ).values_list(
            'field', flat=True
        ).order_by(
            'order_by'
        )
        columns = list(columns)
        return columns

    # def get_values_list(self):
    #     values_list = self.displayed_columns + ['pk', ]
    #     return values_list

    def get_values_list(self):
        values_list = []

        for field in self.displayed_columns:
            if isinstance(field, str) and PERSON_NAME_TOKEN in field:
                prefix = field.replace(PERSON_NAME_TOKEN, '').rstrip('__')

                values_list.extend([
                    f'{prefix}__first_name',
                    f'{prefix}__middle_name',
                    f'{prefix}__last_name',
                    f'{prefix}__salutation',
                ])
            else:
                values_list.append(field)

        values_list.append('pk')

        return values_list


    def get_order_by(self):
        order_by = self.grid.get('order_by', None)
        order_by = [f.strip() for f in order_by.split(',')]
        return order_by


class GridHotelUtility(GridUtility):
    query_filters = {
    }
    hotel_id_field = 'hotel_id'
    event_id_field = 'event_id'

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)
        self.hotel_id = None
        self.hotel_extension: Optional[HotelExtension] = None

    def load_params(self):
        super().load_params()
        self.hotel_id = self.params.get('hotelId', None)
        if not self.hotel_id:
            self.message = 'hotelId is required'
            self.success = False

    def load_models(self):
        super().load_models()
        # hotel_extension = HotelExtension.objects.filter(hotel_id=self.hotel_id).first()
        self.hotel_extension = get_hotel_extension(self.hotel_id)

        if not self.hotel_extension:
            self.message = f'hotel extension not found for hotelId={self.hotel_id}'
            self.success = False

    def get_query_filter(self):
        filters = super().get_query_filter().copy()

        filters[self.hotel_id_field] = self.hotel_id
        # filters['transaction__event_id'] = self.hotel_extension.current_event.event_id

        return filters


class GridEventUtility(GridHotelUtility):
    query_filters = {
    }
    event_id_field = 'event_id'

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)
        self.event_id = None
        self.event: Optional[Event] = None

    def load_params(self):
        super().load_params()

    def load_models(self):
        super().load_models()
        if self.success:
            self.event_id = self.hotel_extension.current_event.event_id
            self.event = Event.objects.filter(event_id=self.event_id).first()
            if not self.event:
                self.message = f'no event associated with hotel'
                self.success = False

    def get_query_filter(self):
        filters = super().get_query_filter().copy()

        filters[self.event_id_field] = self.event_id

        return filters

