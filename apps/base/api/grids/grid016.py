from apps.base.models import HotelCurrency
from constants import process_constants, grid_constants, type_constants, status_constants
from core.api_views.grid_api import AuthorizedGridAPIView, GridSelectAPIView
from core.utilities.grid_utilities import GridUtility


class Grid016Utility(GridUtility):
    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['type_id'] = type_constants.CURRENCY_REAL
        return filters

    def update_selected(self):
        hotel_id = self.params.get('hotelId')

        hotel_currencies = HotelCurrency.objects.filter(hotel_id=hotel_id)

        for hotel_currency in hotel_currencies:
            if hotel_currency.status_id == status_constants.ACTIVE:
                self.rows_df.loc[
                    self.rows_df['pk'] == hotel_currency.currency_id,
                    'selected'
                ] = True

    def get_data_df(self):
        df = super().get_data_df()
        # df.loc[df['form_id'] == '000', 'form__description'] = ''

        return df


class Grid016APIView(GridSelectAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('hotelId',)
    PARAM_OVERRIDES = {
        'hotelId': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }
    process_id = process_constants.GRID_HOTEL_CURRENCY
    grid_id = grid_constants.HOTEL_CURRENCY
    grid_utility_class = Grid016Utility

    param_field = 'hotelId'
    assignment_model = HotelCurrency
    assignment_key_field1 = 'hotel_id'
    assignment_key_field2 = 'currency_id'
