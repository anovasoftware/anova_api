from constants import process_constants, grid_constants
from core.api_views.grid_api import GridHotelAPIView
from core.utilities.grid_utilities import GridHotelUtility
from apps.base.models import Category
from constants import type_constants


class Grid002Utility(GridHotelUtility):
    query_filters = {
        'type_id': type_constants.BASE_CATEGORY_ROOM_CABIN
    }

    # def get_rows_qs(self):
    #     values_list = self.displayed_columns + ['pk', ]
    #
    #     rows = Category.objects.filter(
    #         type_id=type_constants.BASE_CATEGORY_ROOM_CABIN,
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



class Grid002APIView(GridHotelAPIView):
    process_id = process_constants.GRID_ROOM_CATEGORY
    grid_id = grid_constants.ROOM_CATEGORY
    grid_utility_class = Grid002Utility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)