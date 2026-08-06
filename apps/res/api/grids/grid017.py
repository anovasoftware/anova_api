from constants import process_constants, grid_constants
from core.api_views.grid_api import GridHotelAPIView
from core.utilities.grid_utilities import GridHotelUtility
from constants import type_constants


class Grid017Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.RES_EVENT_CRUISE
    }


class Grid017HotelAPIView(GridHotelAPIView):
    process_id = process_constants.GRID_EVENT_SELECT
    grid_id = grid_constants.EVENT_SELECT_FOR_PRICING
    grid_utility_class = Grid017Utility
