from constants import process_constants, grid_constants, type_constants
from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility


class Grid020Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id'] = type_constants.COMPANY_USER_AGENT
        filters['company__client_id'] = self.params.get('clientId', '###')
        return filters


class Grid020APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_COMPANY_USER_AGENT
    grid_id = grid_constants.COMPANY_USER_AGENT
    grid_utility_class = Grid020Utility


