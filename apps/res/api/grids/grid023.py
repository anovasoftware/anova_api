import pandas as pd
from apps.res.models import EventRoom
from apps.static.models import Status
from constants import process_constants, grid_constants, status_constants, type_constants
from core.api_views.grid_api import GridEventAPIView
from core.utilities.grid_utilities import GridEventUtility, GridHotelUtility


class Grid023Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.BASE_CATEGORY_ROOM_CABIN
    }
    hotel_id_field = 'hotel_id'

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)

    def get_data_qs(self):
        queryset = super().get_data_qs()

        return queryset

    def get_data_df(self):
        df = super().get_data_df()
        # summary_df = pd.crosstab(
        #     df['room__category__code'],
        #     df['inventory_status__code']
        # ).reset_index()

        return df

    def post_get_data_df(self):
        displayed_columns = self.displayed_columns
        inventory_statuses = get_inventory_statuses(self.hotel_id)
        dynamic_columns = []

        # Total is always present
        displayed_columns.append('total')
        dynamic_columns.append(
            self.create_grid_column(
                field='total',
                description='Total Cabins',
                label='Total',
                format='number',
            )
        )
        self.rows_df['total'] = 0

        # Status columns
        for status in inventory_statuses:
            status_id = status.status_id
            column = f'status{status_id}'

            displayed_columns.append(column)

            dynamic_columns.append(
                self.create_grid_column(
                    field=column,
                    description=status.description,
                    label=status.code,
                    format='number',
                )
            )

            self.rows_df[column] = 0

        self.displayed_columns = displayed_columns
        self.columns.extend(dynamic_columns)

        # self.add_inventory_counts()

        return


class Grid023APIView(GridEventAPIView):
    process_id = process_constants.GRID_EVENT_ROOM_INVENTORY_SUMMARY
    grid_id = grid_constants.EVENT_ROOM_INVENTORY_SUMMARY
    grid_utility_class = Grid023Utility


def get_inventory_statuses(hotel_id=None):
    statuses = Status.objects.filter(
        grouping='event_room.inventory'
    ).order_by(
        'order_by'
    )
    return statuses
