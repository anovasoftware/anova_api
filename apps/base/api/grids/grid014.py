from constants import process_constants, grid_constants, type_constants
from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility


class Grid014Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id__in'] = [
            type_constants.COMPANY_TRAVEL_AGENCY,
        ]
        filters['client_id'] = self.params.get('clientId', '###')
        return filters


class Grid014APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_COMPANY_TRAVEL_AGENCY
    grid_id = grid_constants.COMPANY_TRAVEL_AGENCY
    grid_utility_class = Grid014Utility


