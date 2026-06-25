from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from constants import process_constants, grid_constants
from core.utilities.grid_utilities import GridUtility


class Grid010Utility(GridUtility):
    pass


class Grid010APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_MENU
    grid_id = grid_constants.GRID_ROLE_MENU
    grid_utility_class = Grid010Utility
