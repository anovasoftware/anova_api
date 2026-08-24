from constants import process_constants, grid_constants, status_constants, client_constants
from core.api_views.grid_api import GridHotelAPIView, AuthorizedGridAPIView
from core.utilities.grid_utilities import GridHotelUtility, GridUtility
from constants import type_constants, hotel_constants, status_constants


class Grid007Utility(GridUtility):
    # query_filters_exclude = {
    #     'type_id': type_constants.NOT_APPLICABLE
    # }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type_id = None
        # self.client_idx = None
        # self.hotel_idx = None

    def load_params(self):
        super().load_params()

        self.type_id = self.params.pop('typeId', None)
        self.query_filters = {'type_id': self.type_id}

        if self.type_id == type_constants.ROLE_HOTEL:
            self.query_filters['hotel_id'] = self.params.pop('hotelId', hotel_constants.NOT_APPLICABLE)
        # self.client_idx = self.params.pop('client_idx', None)
        # self.hotel_idx = self.params.pop('hotel_idx', None)


        # if self.client_idx:
        #     self.query_filters = { 'clientIdx': self.client_idx }
        # elif self.hotel_idx:
        #     self.query_filters = {'hotelIdx': self.hotel_idx}


class Grid007APIView(AuthorizedGridAPIView):
    process_id = process_constants.GRID_ROLE
    grid_id = grid_constants.ROLE
    grid_utility_class = Grid007Utility

    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=False,
            default=None
        ),
    }
    # PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('clientIdx', 'hotelIdx',)
    # PARAM_OVERRIDES = {
    #     'clientIdx': dict(
    #         required_get=False,
    #         required_post=False,
    #         default=None
    #     ),
    #     'hotelIdx': dict(
    #         required_get=False,
    #         required_post=False,
    #         default=None
    #     ),
    #
    # }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_id = None
        # self.client_idx = None
        # self.hotel_idx = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

        # if self.success:
        #     if not self.client_idx and not self.hotel_idx:
        #         message = 'Client id or hotel id are required.'
        #         self.add_message(message=message, http_status_id=status_constants.HTTP_BAD_REQUEST )
