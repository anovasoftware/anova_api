from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from apps.base.models import RoleProcess
from constants import process_constants, grid_constants, type_constants, status_constants
from core.utilities.grid_utilities import GridUtility


class Grid008Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id__in'] = [
            type_constants.PROCESS_ENDPOINT,
            type_constants.PROCESS_ENDPOINT_USER_REQUIRED
        ]
        return filters

    def update_selected(self):
        role_id = self.params.get('roleId')

        role_processs = RoleProcess.objects.filter(role_id=role_id)

        for role_process in role_processs:
            if role_process.status_id == status_constants.ACTIVE:
                self.rows_df.loc[
                    self.rows_df['pk'] == role_process.process_id,
                    'selected'
                ] = True

    def get_data_df(self):
        df = super().get_data_df()
        # df['description'] = (
        #         df['order_by']
        #         .str.count(r'\.')
        #         .map(lambda n: '- - ' * n)
        #         + df['description']
        # )

        return df


class Grid008APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS
    grid_id = grid_constants.ROLE_PROCESS_PROCESS_DRIVEN
    grid_utility_class = Grid008Utility
    assignment_model = RoleProcess
    assignment_field = 'process_id'



    # def _post(self, request):
    #     changes = request.data.get('changes', [])
    #     role_id = self.params.get('roleId')
    #
    #     updated_count = 0
    #     for change in changes:
    #         process_id = change.get('recordId')
    #         selected = change.get('value')
    #
    #         status_id = status_constants.ACTIVE if selected else status_constants.INACTIVE
    #
    #         role_process, created = RoleProcess.objects.update_or_create(
    #             role_id=role_id,
    #             process_id=process_id,
    #             defaults={
    #                 'status_id': status_id
    #             }
    #         )
    #         updated_count += 1
    #
    #     self.set_message('Updated successfully. Records updated: ' + str(updated_count))




# from constants import process_constants, grid_constants
# from core.api_views.grid_api import HotelGridAPIView, AuthorizedGridAPIView
# from core.utilities.grid_utilities import GridHotelUtility, GridUtility
# from constants import type_constants, hotel_constants
#
#
# class Grid008Utility(GridUtility):
#     query_filters_exclude = {
#     }
#
#     # def __init__(self, **kwargs):
#     #     super().__init__(**kwargs)
#     #
#     # def load_params(self):
#     #     super().load_params()
#     #     print(self.params)
#
#     def get_query_filter(self):
#         filters = super().get_query_filter()
#
#         role_id = self.params.get('roleId')
#
#         if role_id:
#             filters['role_id'] = role_id
#
#         return filters
#
#
# class Grid008APIView(AuthorizedGridAPIView):
#     process_id = process_constants.GRID_ROLE_PROCESS
#     grid_id = grid_constants.ROLE_PROCESS
#     grid_utility_class = Grid008Utility
#
#     PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('roleId',)
#     PARAM_OVERRIDES = {
#         'roleId': dict(
#             required_get=True,
#             required_post=True,
#             default=None
#         ),
#     }
#
#
