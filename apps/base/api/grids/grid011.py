from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from apps.base.models import RoleMenu
from constants import process_constants, grid_constants, type_constants, status_constants
from core.utilities.grid_utilities import GridUtility


class Grid011Utility(GridRoleUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        return filters


class Grid011APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS_DETAIL
    grid_id = grid_constants.ROLE_PROCESS_DETAIL
    grid_utility_class = Grid011Utility

