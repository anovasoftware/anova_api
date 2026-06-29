from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from apps.base.models import RoleMenu
from constants import process_constants, grid_constants, type_constants, status_constants
from core.utilities.grid_utilities import GridUtility


class Grid010Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id__in'] = [
            type_constants.MENU_NAVIGATION
        ]
        return filters

    def update_selected(self):
        role_id = self.params.get('roleId')

        role_menus = RoleMenu.objects.filter(role_id=role_id)

        # for role_menu in role_menus:
        #     self.rows_df.loc[self.rows_df['pk'] == role_menu.menu_id, 'selected'] = True

        for role_menu in role_menus:
            if role_menu.status_id == status_constants.ACTIVE:
                self.rows_df.loc[
                    self.rows_df['pk'] == role_menu.menu_id,
                    'selected'
                ] = True

    def get_data_df(self):
        df = super().get_data_df()
        df['description'] = (
                df['order_by']
                .str.count(r'\.')
                .map(lambda n: '- - ' * n)
                + df['description']
        )

        return df


class Grid010APIView(GridRoleAPIView):
    process_id = process_constants.GRID_ROLE_MENU
    grid_id = grid_constants.ROLE_MENU
    grid_utility_class = Grid010Utility
    assignment_model = RoleMenu
    assignment_field = 'menu_id'

    # def _post(self, request):
    #     changes = request.data.get('changes', [])
    #     role_id = self.params.get('roleId')
    #
    #     updated_count = 0
    #     for change in changes:
    #         menu_id = change.get('recordId')
    #         selected = change.get('value')
    #
    #         status_id = status_constants.ACTIVE if selected else status_constants.INACTIVE
    #
    #         role_menu, created = RoleMenu.objects.update_or_create(
    #             role_id=role_id,
    #             menu_id=menu_id,
    #             defaults={
    #                 'status_id': status_id
    #             }
    #         )
    #         updated_count += 1
    #
    #     self.set_message('Updated successfully. Records updated: ' + str(updated_count))
