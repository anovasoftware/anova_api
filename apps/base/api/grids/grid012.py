from apps.base.api.grids.grid_role import GridRoleUtility, GridSelectRoleAPIView
from apps.base.api.grids.grid_role_process import GridRoleProcessUtility
from apps.base.models import RoleProcess
from constants import process_constants, grid_constants, type_constants, status_constants


class Grid012Utility(GridRoleProcessUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id__in'] = [
            type_constants.PROCESS_GRID,
        ]
        return filters


class Grid012APIView(GridSelectRoleAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS_GRID
    grid_id = grid_constants.ROLE_PROCESS_GRID
    grid_utility_class = Grid012Utility

    assignment_model = RoleProcess
    assignment_key_field2 = 'process_id'
