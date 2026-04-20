from constants import process_constants, grid_constants, status_constants
from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility
from constants import type_constants


class Grid001Utility(GridUtility):
    query_filters = {
        'status_id__in': [
            status_constants.USER_ACTIVE,
            status_constants.USER_PENDING,
            status_constants.USER_LOCKED,
            status_constants.USER_DELETED,
        ],
        'type_id': type_constants.USER_REAL
    }
    remove_filters = ['status_id']

    # def get_rows_qs(self):
    #     filters = self.get_query_filter()
    #     rows = self.base_model.objects.filter(
    #         **filters
    #     )
    #
    #     rows = rows.values(
    #         *self.values_list,
    #     ).order_by(
    #         *self.order_by
    #     )
    #     rows = list(rows)
    #
    #     return rows

    # def get_query_filter(self):
    #     filters = super().get_query_filter()
    #     for remove_filter in self.remove_filters:
    #         filters.pop(remove_filter, None)
    #     filters.update(self.query_filters)
    #     return filters


class Grid001APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_USER_ANOVA
    grid_id = grid_constants.USER_ANOVA
    grid_utility_class = Grid001Utility
