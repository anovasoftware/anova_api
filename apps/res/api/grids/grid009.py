from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView
from core.utilities.grid_utilities import GridEventUtility, GridHotelUtility


class Grid009Utility(GridHotelUtility):
    query_filters = {
    }
    # remove_filters = ['status_id']
    # hotel_id_field = 'transaction__hotel_id'
    # event_id_field = 'transaction__event_id'
    #
    # def get_query_filter(self):
    #     filters = super().get_query_filter().copy()
    #     # filters['transaction__event_id'] = self.hotel_extension.current_event.event_id
    #
    #     return filters

class Grid009APIView(HotelGridAPIView):
    process_id = process_constants.GRID_FLOOR
    grid_id = grid_constants.FLOOR
    grid_utility_class = Grid009Utility





