from core.api_views.core_api import CoreAPIView
from core.api_views.core_api import AuthorizedAPIView
from constants import status_constants
from core.utilities.grid_utilities import GridUtility


class GridAPIView(CoreAPIView):
    grid_id = None
    grid_utility_class = GridUtility

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if self.success and not self.grid_id:
            message = f'{self.__class__.__name__} requires grid_id but none was defined.'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def _get(self, request):
        if self.success:
            try:
                self.grid = self.grid_utility_class(self.grid_id).get_grid()
                self.data['grid'] = self.grid
            except Exception as e:
                message = 'not defined'
                self.add_message(message, http_status_id='VALIDATION_ERROR')

    def build_response(self):
        response = super().build_response()

        # if self.is_get():
        #     self.records = transform_records(self.records, shape=self.result_shape)
        #     record_count = len(self.records)
        #
        #     if 'form' not in self.data:
        #         self.data['record_count'] = record_count
        #         self.data['records'] = self.records
        # if self.type:
        #     response['context']['type_id'] = self.type.type_id
        #     response['context']['type_description'] = self.type.description

        return response



class PublicGridAPIView(GridAPIView):
    pass


class AuthorizedGridAPIView(GridAPIView, AuthorizedAPIView):
    pass
