from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
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

    # def update_selected(self):
    #     role_id = self.params.get('roleId')
    #
    #     role_processes = RoleProcess.objects.filter(role_id=role_id)
    #
    #     for role_process in role_processes:
    #         if role_process.status_id == status_constants.ACTIVE:
    #             self.rows_df.loc[
    #                 self.rows_df['pk'] == role_process.process_id,
    #                 'selected'
    #             ] = True
    #
    #     self.rows_df['selected_disabled'] = (
    #             self.rows_df['user_required_flag'] != 'Y'
    #     )
    #     self.rows_df['selected'] = (
    #             self.rows_df['user_required_flag'] != 'Y'
    #     )
    #
    # def get_data_df(self):
    #     df = super().get_data_df()
    #     df.loc[df['form_id'] == '000', 'form__description'] = ''
    #
    #     return df


class Grid012APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_PROCESS_GRID
    grid_id = grid_constants.ROLE_PROCESS_GRID
    grid_utility_class = Grid012Utility
    assignment_model = RoleProcess
    assignment_field = 'process_id'
