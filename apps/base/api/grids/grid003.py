from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView
from core.utilities.grid_utilities import GridHotelUtility
from apps.res.models import Room
from constants import type_constants


class Grid003Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.RES_ROOM_CABIN
    }


    # def get_rows_qs(self):
    #     values_list = self.displayed_columns + ['pk', ]
    #
    #     rows = Room.objects.filter(
    #         # type_id=type_constants.ROO
    #         hotel_id=self.hotel_id
    #     )
    #
    #     rows = rows.values(
    #         *values_list,
    #         # 'username',
    #         # 'person__first_name',
    #         # 'pk'
    #     ).order_by(
    #         'description'
    #     )
    #     rows = list(rows)
    #
    #     return rows


class Grid003APIView(HotelGridAPIView):
    process_id = process_constants.GRID_ROOM
    grid_id = grid_constants.ROOM
    grid_utility_class = Grid003Utility
