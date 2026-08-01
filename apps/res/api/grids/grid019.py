from botocore.docs import params

from apps.base.models import HotelCurrency
from constants import process_constants, grid_constants, currency_constants, type_constants, status_constants
from core.api_views.grid_api import EventGridAPIView
from core.utilities.grid_utilities import GridEventUtility, GridHotelUtility
from django.db.models import F


class Grid019Utility(GridHotelUtility):
    query_filters = {
    }

    hotel_id_field = 'hotel_id'

    def get_query_filter(self):
        filters = super().get_query_filter()
        # filters['event_id'] = self.params.get('eventId')
        # filters['currency_id'] = currency_constants.USD
        # filters['rate_type'] = type_constants.EVENT_CATEGORY_PRICE_RATE_FIT
        return filters

    def get_data_df(self):
        rows_df = super().get_data_df()

        if self.success:
            df = rows_df.copy()

        return rows_df

    def load_lookups(self):
        super().load_lookups()
        self.add_lookup(
            lookup_name='lookup1',
            label='Currency',
            options=self.get_currency_lookup(),
            selected_id=self.hotel_extension.currency_id
        )


class Grid019APIView(EventGridAPIView):
    process_id = process_constants.GRID_EVENT_GRADE_PRICE
    grid_id = grid_constants.EVENT_CATEGORY_PRICE
    grid_utility_class = Grid019Utility

