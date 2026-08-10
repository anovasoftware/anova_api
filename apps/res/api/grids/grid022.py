from apps.res.models import EventRoom
from constants import process_constants, grid_constants, status_constants
from core.api_views.grid_api import GridEventAPIView
from core.utilities.grid_utilities import GridEventUtility


class Grid022Utility(GridEventUtility):
    query_filters = {
        # 'type_id': type_constants.RES_EVENT_CRUISE
    }
    hotel_id_field = 'event__hotel_id'

    def __init__(self, grid_id, params=None):
        super().__init__(grid_id, params)

        EventRoom.objects.filter(
            status_id=status_constants.EVENT_ROOM_AVAILABLE
        ).update(
            status_id=status_constants.ACTIVE
        )




class Grid022APIView(GridEventAPIView):
    process_id = process_constants.GRID_EVENT_ROOM_INVENTORY
    grid_id = grid_constants.EVENT_ROOM_INVENTORY
    grid_utility_class = Grid022Utility
