from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView
from core.utilities.grid_utilities import GridHotelUtility
from constants import type_constants


class Grid006Utility(GridHotelUtility):
    query_filters = {
        # 'type_id': type_constants.RES_EVENT_CRUISE
    }
    remove_filters = ['status_id']


class Grid006APIView(HotelGridAPIView):
    process_id = process_constants.GRID_TRANSACTION_STAGED
    grid_id = grid_constants.TRANSACTION_STAGED
    grid_utility_class = Grid006Utility


