from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView, AuthorizedGridAPIView
from core.utilities.grid_utilities import GridHotelUtility, GridUtility
from constants import type_constants, hotel_constants


class Grid008Utility(GridUtility):
    query_filters_exclude = {
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hotel_idx = None

class Grid008APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS
    grid_id = grid_constants.ROLE_PROCESS
    grid_utility_class = Grid008Utility

