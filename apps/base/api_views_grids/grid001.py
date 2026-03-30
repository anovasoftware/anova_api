from constants import process_constants, grid_constants
from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility


class Grid001Utility(GridUtility):
    pass


class Grid001APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_USER_ANOVA
    grid_id = grid_constants.USER_ANOVA
    grid_utility_class = Grid001Utility
