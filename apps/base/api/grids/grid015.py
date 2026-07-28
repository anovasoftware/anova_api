from apps.base.api.grids.grid_role import GridRoleUtility, GridRoleAPIView
from apps.base.models import RoleProcess, ClientCurrency
from constants import process_constants, grid_constants, type_constants, status_constants
from core.api_views.grid_api import AuthorizedGridAPIView, GridSelectAPIView
from core.utilities.grid_utilities import GridUtility


class Grid015Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id'] = type_constants.CURRENCY_REAL
        return filters

    def update_selected(self):
        client_id = self.params.get('clientId')

        client_currencies = ClientCurrency.objects.filter(client_id=client_id)

        for client_currency in client_currencies:
            if client_currency.status_id == status_constants.ACTIVE:
                self.rows_df.loc[
                    self.rows_df['pk'] == client_currency.currency_id,
                    'selected'
                ] = True

        # self.rows_df['selected_disabled'] = (
        #         self.rows_df['user_required_flag'] != 'Y'
        # )
        # self.rows_df['selected'] = (
        #         self.rows_df['user_required_flag'] != 'Y'
        # )

    def get_data_df(self):
        df = super().get_data_df()
        # df.loc[df['form_id'] == '000', 'form__description'] = ''

        return df


class Grid015APIView(GridSelectAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('clientId',)
    PARAM_OVERRIDES = {
        'clientId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }
    process_id = process_constants.GRID_CLIENT_CURRENCY
    grid_id = grid_constants.CLIENT_CURRENCY
    grid_utility_class = Grid015Utility

    assignment_model = ClientCurrency
    assignment_lookup_field = 'currency_id'
    assignment_record_field = 'currency_id'
    param_field = 'clientId'
