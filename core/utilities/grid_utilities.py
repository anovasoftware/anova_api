import pandas as pd
from apps.static.models import Grid, GridColumn
from core.utilities.string_utilities import field_to_data_path


class GridUtility(object):
    def __init__(self, grid_id, params=None):
        self.grid_id = grid_id
        self.params = {} or params
        self.grid = None

        self.columns = None
        self.rows_qs = None
        self.rows_df = None
        self.rows = None
        self.displayed_columns = None

        self.success = True
        self.message = 'grid loaded'

        # self.load_grid()

    def load_grid(self):
        self.grid = self.get_grid()
        self.columns = self.get_columns()

        if self.success:
            self.displayed_columns = self.get_displayed_columns()
            self.rows_qs = self.get_rows_qs()
            if self.success:
                self.rows_df = self.get_rows_df()
                if self.success:
                    self.rows = self.get_rows()
                    if self.success:
                        self.grid['displayed_columns'] = self.displayed_columns
                        self.grid['columns'] = self.columns
                        self.grid['rows'] = self.rows

    def get_grid(self):
        grid = Grid.objects.values(
            'grid_id',
            'description',
            'title'
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
            columns_df['data_path'] = columns_df['field'].apply(field_to_data_path)
            columns = columns_df.to_dict('records')
        else:
            self.message = 'no columns found'
            self.success = False

        return columns

    def get_rows_qs(self):
        self.message = 'get_rows_qs not defined'
        self.success = False
        return []

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
        return list(columns)


class GridHotelUtility(GridUtility):
    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)
        self.hotel_id = self.params.get('hotelId', None)
