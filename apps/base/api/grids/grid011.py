from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from constants import process_constants, grid_constants, type_constants


class Grid011Utility(GridRoleUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['process__type_id__in'] = [
            type_constants.PROCESS_FORM,
        ]
        return filters


class Grid011APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS_DETAIL
    grid_id = grid_constants.ROLE_PROCESS_DETAIL
    grid_utility_class = Grid011Utility

