from constants import process_constants, grid_constants, currency_constants, type_constants
from core.api_views.grid_api import GridEventAPIView
from core.utilities.grid_utilities import GridHotelUtility



class Grid018Utility(GridHotelUtility):
    query_filters = {
        # 'event_id': params.get('event_id')
    }

    hotel_id_field = 'event__hotel_id'

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['event_id'] = self.params.get('eventId')
        filters['currency_id'] = currency_constants.USD
        filters['rate_type'] = type_constants.EVENT_CATEGORY_PRICE_RATE_FIT
        return filters

    def get_data_df(self):
        rows_df = super().get_data_df()

        if self.success:
            df = rows_df.copy()

        return rows_df

class Grid018EventAPIView(GridEventAPIView):
    process_id = process_constants.GRID_EVENT_GRADE_PRICE
    grid_id = grid_constants.EVENT_CATEGORY_PRICE
    grid_utility_class = Grid018Utility

