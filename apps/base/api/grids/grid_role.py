from core.api_views.grid_api import AuthorizedGridAPIView
from core.utilities.grid_utilities import GridUtility
from constants import process_constants, grid_constants, type_constants, status_constants


class GridRoleUtility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()

        role_id = self.params.get('roleId')

        if role_id:
            filters['role_id'] = role_id

        return filters


class GridRoleAPIView(AuthorizedGridAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('roleId',)
    PARAM_OVERRIDES = {
        'roleId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }
    assignment_model = None
    assignment_field = None


    def _post(self, request):
        changes = request.data.get('changes', [])
        role_id = self.params.get('roleId')

        updated_count = 0

        for change in changes:
            record_id = change.get('recordId')
            selected = change.get('value')

            status_id = status_constants.ACTIVE if selected else status_constants.INACTIVE

            self.assignment_model.objects.update_or_create(
                role_id=role_id,
                **{self.assignment_field: record_id},
                defaults={'status_id': status_id}
            )

            updated_count += 1

        self.set_message(f'Updated successfully. Records updated: {updated_count}')