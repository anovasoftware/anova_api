from constants import process_constants, grid_constants
from core.api_views.grid_api import HotelGridAPIView, AuthorizedGridAPIView
from core.utilities.grid_utilities import GridHotelUtility, GridUtility
from constants import type_constants, hotel_constants


class Grid007Utility(GridUtility):
    query_filters_exclude = {
        'type_id': type_constants.NOT_APPLICABLE
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hotel_idx = None

    def load_params(self):
        super().load_params()

        self.hotel_idx = self.params.pop('hotelIdx', hotel_constants.NOT_APPLICABLE)

        self.query_filters = {
            'hotel_id__in': [
                self.hotel_idx
            ]
        }


class Grid007APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_ROLE
    grid_id = grid_constants.ROLE
    grid_utility_class = Grid007Utility

    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('hotelIdx',)
    PARAM_OVERRIDES = {
        'hotelIdx': dict(
            required_get=True,
            required_post=True,
            default=None
        ),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hotel_idx = None

    # def load_request(self, request, *args, **kwargs):
    #     super().load_request(request, *args, **kwargs)
    #
    #     print(self.hotel_idx)
