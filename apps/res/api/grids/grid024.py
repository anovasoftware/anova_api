from constants import process_constants, grid_constants
from core.api_views.grid_api import GridEventAPIView, GridHotelAPIView
from core.utilities.grid_utilities import GridEventUtility, GridHotelUtility


class Grid024Utility(GridHotelUtility):
    query_filters = {
        # 'type_id': type_constants.RES_EVENT_CRUISE
    }
    hotel_id_field = 'hotel_id'

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)




class Grid024APIView(GridHotelAPIView):
    process_id = process_constants.GRID_BOOKINGS
    grid_id = grid_constants.BOOKINGS
    grid_utility_class = Grid024Utility
