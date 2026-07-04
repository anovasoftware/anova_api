from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from apps.base.models import RoleProcess
from constants import process_constants, grid_constants, type_constants, status_constants
from core.utilities.grid_utilities import GridUtility


class GridRoleProcessUtility(GridUtility):
    def update_selected(self):
        role_id = self.params.get('roleId')

        role_processes = RoleProcess.objects.filter(role_id=role_id)

        for role_process in role_processes:
            if role_process.status_id == status_constants.ACTIVE:
                self.rows_df.loc[
                    self.rows_df['pk'] == role_process.process_id,
                    'selected'
                ] = True

        self.rows_df['selected_disabled'] = (
                self.rows_df['user_required_flag'] != 'Y'
        )
        self.rows_df['selected'] = (
                self.rows_df['user_required_flag'] != 'Y'
        )
