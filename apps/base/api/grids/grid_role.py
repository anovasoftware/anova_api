from core.api_views.grid_api import AuthorizedGridAPIView, GridSelectAPIView
from core.utilities.grid_utilities import GridUtility


class GridRoleUtility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()

        role_id = self.params.get('roleId')

        if role_id:
            filters['role_id'] = role_id

        return filters


class GridSelectRoleAPIView(GridSelectAPIView):
    PARAM_NAMES = GridSelectAPIView.PARAM_NAMES + ('roleId',)
    PARAM_OVERRIDES = {
        **GridSelectAPIView.PARAM_OVERRIDES,
        'roleId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }
    param_field = 'roleId'
    assignment_model = None
    assignment_key_field1 = 'role_id'
    assignment_key_field2 = None


class GridRoleAPIView(AuthorizedGridAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('roleId',)
    PARAM_OVERRIDES = {
        **AuthorizedGridAPIView.PARAM_OVERRIDES,
        'roleId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }
    # param_field = 'roleId'
    # assignment_model = None
    # assignment_key_field1 = 'role_id'
    # assignment_key_field2 = None
