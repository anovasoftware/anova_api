import pandas as pd
from apps.static.models import Grid, GridColumn
from constants import status_constants
from django.apps import apps
from typing import Optional
from django.db.models import Model
from core.utilities.data_transformation_utilities import snake_to_camel_list, snake_to_camel


class GridUtility(object):
    remove_filters = []
    query_filters = {}

    def __init__(self, grid_id, params=None):
        self.grid_id = grid_id
        self.params = {} or params
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

        # self.load_grid()

    def load_grid(self):
        self.grid = self.get_grid()
        self.columns = self.get_columns()

        app_name = self.grid['data_source_application']
        model_name = self.grid['data_source_model_name']
        self.base_model = apps.get_model(app_name, model_name)

        if self.success:
            self.displayed_columns = self.get_displayed_columns()
            self.values_list = self.get_values_list()
            self.order_by = self.get_order_by()

            self.rows_qs = self.get_rows_qs()
            if self.success:
                self.rows_df = self.get_rows_df()
                if self.success:
                    self.rows = self.get_rows()
                    if self.success:
                        remove_keys = [
                            'data_source_application',
                            'data_source_model_name',
                            'order_by'
                        ]
                        self.grid = {k: v for k, v in self.grid.items() if k not in remove_keys}

                        # transform data
                        self.displayed_columns = snake_to_camel_list(self.displayed_columns, '_')
                        # for column in self.columns:
                        #     column['field'] = snake_to_camel(column['field'], '_')

                        self.grid['displayed_columns'] = snake_to_camel_list(self.displayed_columns,'.')
                        self.grid['columns'] = self.columns
                        self.grid['rows'] = self.rows

    def get_grid(self):
        grid = Grid.objects.values(
            'grid_id',
            'description',
            'title',
            'data_source_application',
            'data_source_model_name',
            'order_by'
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
            grid_id=self.grid_id
        ).order_by(
            'order_by'
        )
        columns_df = pd.DataFrame(list(columns_qs))

        if not columns_df.empty:
            # columns_df['data_path'] = columns_df['field'].apply(field_to_data_path)
            # columns_df['data_path'] = columns_df['field'].apply(snake_to_camel)

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

        return columns

    # def get_query_filter(self):
    #     filters = {
    #         'status_id': status_constants.ACTIVE,
    #     }
    #
    #     return filters  # This will be used in queryset.filter()

    def get_query_filter(self):
        filters = {
            'status_id': status_constants.ACTIVE,
        }

        for remove_filter in self.remove_filters:
            filters.pop(remove_filter, None)
        filters.update(self.query_filters)
        return filters


    def get_rows_qs(self):
        filters = self.get_query_filter()
        rows = self.base_model.objects.filter(
            **filters
        )

        rows = rows.values(
            *self.values_list,
        ).order_by(
            *self.order_by
        )
        rows = list(rows)

        return rows

    def get_rows_df(self):
        rows_df = pd.DataFrame(list(self.rows_qs))
        return rows_df

    def get_rows(self):
        rows = self.rows_df.to_dict('records')
        return rows

    def get_displayed_columns(self):
        columns = GridColumn.objects.filter(
            grid_id=self.grid_id,
        ).values_list(
            'field', flat=True
        )
        columns = list(columns)
        # columns = format_response(columns)
        return list(columns)

    def get_values_list(self):
        values_list = self.displayed_columns + ['pk', ]
        return values_list

    def get_order_by(self):
        order_by = self.grid.get('order_by', None)
        order_by = [f.strip() for f in order_by.split(',')]
        return order_by


class GridHotelUtility(GridUtility):
    query_filters = {
    }

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)
        self.hotel_id = self.params.get('hotelId', None)

    def get_query_filter(self):
        filters = super().get_query_filter().copy()

        # add dynamic hotel filter
        if self.hotel_id:
            filters['hotel_id'] = self.hotel_id

        return filters