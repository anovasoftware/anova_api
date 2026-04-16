from constants import process_constants, grid_constants
from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility
from apps.base.models import User
from constants import type_constants


class Grid001Utility(GridUtility):
    def get_rows_qs(self):
        values_list = self.displayed_columns + ['pk', ]

        rows = User.objects.filter(
            type_id=type_constants.USER_REAL
        )

        rows = rows.values(
            *values_list,
            # 'username',
            # 'person__first_name',
            # 'pk'
        ).order_by(
            'username'
        )
        rows = list(rows)

        return rows



class Grid001APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_USER_ANOVA
    grid_id = grid_constants.USER_ANOVA
    grid_utility_class = Grid001Utility
