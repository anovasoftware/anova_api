from decimal import Decimal

from constants import process_constants, grid_constants, type_constants, currency_constants, event_constants, \
    status_constants
from core.api_views.grid_api import GridEventAPIView, GridUpdateMixin
from core.utilities.grid_utilities import GridHotelUtility
from apps.static.models import Type
from apps.res.models import EventCategoryPrice

class Grid019Utility(GridHotelUtility):
    query_filters = {
    }

    hotel_id_field = 'hotel_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_id = None
        self.currency_id = None
        self.rate_type_id = None


    # def load_params(self):
    #     super().load_params()
    #
    #     if self.success:
    #         self.event_id = self.params.get('eventId', event_constants.NOT_APPLICABLE)
    #         self.currency_id = self.params.get('currencyId', self.get_hotel_currency_id())
    #         self.rate_type_id = self.params.get('rateTypeId', type_constants.EVENT_CATEGORY_PRICE_RATE_FIT)

    def load_models(self):
        super().load_models()

        if self.success:
            self.event_id = self.params.get('eventId', event_constants.NOT_APPLICABLE)
            self.currency_id = self.params.get('currencyId', self.get_client_currency_id())
            self.rate_type_id = self.params.get('rateTypeId', type_constants.EVENT_CATEGORY_PRICE_RATE_FIT)

    def get_query_filter(self):
        filters = super().get_query_filter()
        # filters['event_id'] = self.params.get('eventId')
        # filters['currency_id'] = currency_constants.USD
        # filters['rate_type'] = type_constants.EVENT_CATEGORY_PRICE_RATE_FIT
        return filters

    def get_data_df(self):
        rows_df = super().get_data_df()

        if self.success:
            df = rows_df.copy()

        return rows_df

    def load_lookups(self):
        super().load_lookups()
        self.add_lookup(
            lookup_name='lookup1',
            param_name='currencyId',
            label='Currency',
            options=self.get_client_currency_lookup(),
            selected_id=self.get_client_currency_id()
        )
        self.add_lookup(
            lookup_name='lookup2',
            param_name='rateTypeId',
            label='Rate Type',
            options=self.get_rate_type_lookup(),
            selected_id=type_constants.EVENT_CATEGORY_PRICE_RATE_FIT
        )

    def post_get_data_df(self):
        displayed_columns = self.displayed_columns
        occupancy_types = self.get_occupancy_types()
        dynamic_columns = []

        for occupancy_type in occupancy_types:
            occupancy_type_id = occupancy_type.type_id
            column = f'price{occupancy_type_id}'

            displayed_columns.append(column)
            dynamic_columns.append(
                self.create_grid_column(
                    field=column,
                    description=occupancy_type.description,
                    label=occupancy_type.code,
                    format='currency',
                    editable=True,
                )
            )
            # initialize to 0.00
            self.rows_df[column] = Decimal(-1)

        self.displayed_columns = displayed_columns
        self.columns.extend(dynamic_columns)
        self.add_occupancy_prices()

        return

    def add_occupancy_prices(self):
        rows_df = self.rows_df

        event_category_prices = EventCategoryPrice.objects.filter(
            event_id=self.event_id,
            currency_id=self.currency_id,
            rate_type_id=self.rate_type_id,
        )

        if not event_category_prices.exists():
            self.success = False
            self.message = f'Pricing has not been configured for currency {self.currency_id}'
        else:
            for event_category_price in event_category_prices:
                column = f'price{event_category_price.occupancy_type_id}'
                category_id = event_category_price.category_id

                rows_df.loc[rows_df['pk'] == category_id, column] = event_category_price.price

        self.rows_df = rows_df

class Grid019EventAPIView(GridUpdateMixin, GridEventAPIView):
    process_id = process_constants.GRID_EVENT_GRADE_PRICE
    grid_id = grid_constants.EVENT_CATEGORY_PRICE
    grid_utility_class = Grid019Utility

    PARAM_NAMES = GridEventAPIView.PARAM_NAMES + ('currencyId', 'rateTypeId')
    PARAM_OVERRIDES = {
        'currencyId': dict(
            required_get=False,
            required_post=True,
            # default=currency_constants.TO_BE_ANNOUNCED,
        ),
        'rateTypeId': dict(
            required_get=True,
            required_post=True,
            default=type_constants.EVENT_CATEGORY_PRICE_RATE_FIT,
        ),
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.currency_id = None
        self.rate_type_id = None

    def _post(self, request):
        updated_count = self.process_changes(request)

        self.set_message(
            f'Updated successfully. Records updated: {updated_count}'
        )

    def save_change(self, change):
        category_id = change.get('recordId')
        field = change.get('field')
        price = change.get('value')

        if not category_id:
            self.add_message(message=f'Category id is required.', http_status_id=status_constants.HTTP_BAD_REQUEST)

        if not field or not field.startswith('price'):
            self.add_message(message=f'Field is required.', http_status_id=status_constants.HTTP_BAD_REQUEST)

        if self.success:
            occupancy_type_id = field.removeprefix('price')

            try:
                event_category_price = EventCategoryPrice.objects.get(
                    event_id=self.event_id,
                    category_id=category_id,
                    occupancy_type_id=occupancy_type_id,
                    currency_id=self.currency_id,
                    rate_type_id=self.params.get('rateTypeId'),
                )

                event_category_price.price = price
                event_category_price.save()
            except Exception as e:
                message = f'Failed to update event category price. Error: {e}'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)


        return self.success