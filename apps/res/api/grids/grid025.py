from constants import process_constants, grid_constants
from core.api_views.grid_api import GridHotelAPIView, GridEventAPIView
from core.utilities.grid_utilities import GridHotelUtility
from constants import type_constants


class Grid025Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.RES_EVENT_CRUISE
    }

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)

        self.column_grid_id = grid_constants.SELECT_EVENT_FOR_PRICING


class Grid025APIView(GridHotelAPIView):
    process_id = process_constants.GRID_EVENT_BOOKING
    grid_id = grid_constants.SELECT_EVENT_FOR_BOOKING
    grid_utility_class = Grid025Utility
