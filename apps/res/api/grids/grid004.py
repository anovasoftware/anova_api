from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView
from core.utilities.grid_utilities import GridHotelUtility
from constants import type_constants


class Grid004Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.RES_EVENT_CRUISE
    }


class Grid004APIView(HotelGridAPIView):
    process_id = process_constants.GRID_EVENT
    grid_id = grid_constants.EVENT
    grid_utility_class = Grid004Utility
