from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView
from core.utilities.grid_utilities import GridHotelUtility
from constants import type_constants


class Grid005Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.BASE_POSITION_ONBOARD
    }


class Grid005APIView(HotelGridAPIView):
    process_id = process_constants.GRID_POSITION
    grid_id = grid_constants.POSITION
    grid_utility_class = Grid005Utility
