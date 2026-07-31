from core.api_views.core_api import CoreAPIView
from core.api_views.core_api import AuthorizedAPIView
from constants import status_constants
from core.utilities.grid_utilities import GridUtility


class GridAPIView(CoreAPIView):
    grid_id = None
    grid_utility_class = GridUtility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if self.success and not self.grid_id:
            message = f'{self.__class__.__name__} requires grid_id but none was defined.'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def _get(self, request):
        utility = self.grid_utility_class(grid_id=self.grid_id, params=self.params)
        if self.success:
            utility.load_grid()
            if not self.success:
                self.add_message(utility.message, status_constants.HTTP_BAD_REQUEST)
        if self.success:
            try:

                self.grid = utility.grid
                if not utility.success:
                    self.add_message(utility.message, status_constants.HTTP_BAD_REQUEST)
                # grid = self.grid_utility_class(self.grid_id).get_grid()
                # columns = self.grid_utility_class(self.grid_id).get_grid_columns()
                # rows = self.grid_utility_class(self.grid_id).get_grid_rows()
                # displayed_columns = self.grid_utility_class(self.grid_id).get_displayed_columns()
                # grid['columns'] = columns
                # grid['rows'] = rows
                # grid['displayed_columns'] = displayed_columns
                #
                # self.grid = grid

                self.data['grid'] = self.grid
            except Exception as e:
                message = 'not defined'
                self.add_message(message, http_status_id='VALIDATION_ERROR')

        self.utility = utility

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


class AuthorizedGridAPIView(AuthorizedAPIView, GridAPIView):
    pass


class HotelGridAPIView(AuthorizedGridAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('hotelId', )
    PARAM_OVERRIDES = {
        'hotelId': dict(
            required_get=True,
            required_post=True,
            required_patch=True,
            default=None
        ),
        # 'debugFlag': dict(required_get=True, allowed=('Y', 'N'))
    }


class EventGridAPIView(AuthorizedGridAPIView):
    PARAM_NAMES = AuthorizedGridAPIView.PARAM_NAMES + ('eventId', )
    PARAM_OVERRIDES = {
        'eventId': dict(
            required_get=True,
            required_post=True,
            required_patch=True,
            default=None
        ),
        # 'debugFlag': dict(required_get=True, allowed=('Y', 'N'))
    }

# class GridSelectAPIView(AuthorizedGridAPIView):
#     assignment_model = None
#     assignment_field = None
#     param_field = None
#
#
#     def _post(self, request):
#         changes = request.data.get('changes', [])
#         role_id = self.params.get(self.param_field)
#
#         updated_count = 0
#
#         for change in changes:
#             record_id = change.get('recordId')
#             selected = change.get('value')
#
#             status_id = status_constants.ACTIVE if selected else status_constants.INACTIVE
#
#             self.assignment_model.objects.update_or_create(
#                 role_id=role_id,
#                 **{self.assignment_field: record_id},
#                 defaults={'status_id': status_id}
#             )
#
#             updated_count += 1
#
#         self.set_message(f'Updated successfully. Records updated: {updated_count}')
class GridSelectAPIView(AuthorizedGridAPIView):
    param_field = None                # e.g. 'roleId'
    assignment_model = None
    assignment_key_field1 = None      # e.g. 'role_id'
    assignment_key_field2 = None      # e.g. 'process_id'


    def _post(self, request):
        changes = request.data.get('changes', [])
        key_field1_value = self.params.get(self.param_field)

        updated_count = 0

        for change in changes:
            record_id = change.get('recordId')
            selected = change.get('value')
            status_id = status_constants.ACTIVE if selected else status_constants.INACTIVE
            key_fields = self.get_key_fields(key_field1_value=key_field1_value, key_field2_value=record_id)
            print(self.grid_id, self.assignment_model, key_fields)
            self.assignment_model.objects.update_or_create(
                **key_fields,
                defaults={
                    'status_id': status_id,
                }
            )

            updated_count += 1

        self.set_message(f'Updated successfully. Records updated: {updated_count}'
        )

    def get_key_fields(self, key_field1_value=None, key_field2_value=None):
        key_fields = {
            self.assignment_key_field1: key_field1_value,
            self.assignment_key_field2: key_field2_value,
        }

        return key_fields
