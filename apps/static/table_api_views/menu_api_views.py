from core.api_views.table_api_views import PublicTableAPIView
from apps.static.models import Menu
from constants import type_constants, status_constants, process_constants


class PublicMenuAPIView(PublicTableAPIView):
    process_id = None

    PARAM_SPECS = PublicTableAPIView.PARAM_SPECS + ('typeId', )
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=False,
            required_post=False,
            allowed=(
                'ALL'
            )
        )
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'static'
        self.model_name = 'Menu'
        self.type_id = 'ALL'
        self.menu_id = None
        self.menu = None
        # self.accepted_type_ids = [
        #     'ALL'
        #     # type_constants.MENU_HEADER_BAR
        # ]

        self.user = None

    def load_request(self, request):
        super().load_request(request)

        # if self.menu_id:
        #     try:
        #         self.menu = Menu.objects.filter(type_id=self.type_id)
        #     except Exception as e:
        #         self.set_message(f'room not found: {self.user_id}', success=False)

    def get_value_list(self):
        value_list = [
            'menu_id',
            'type_id',
            'description',
            'title',
            'sub_title',
            'breadcrumb_name',
            'route',
            'page__page_id',
            'page__description',
        ]

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['status_id'] = status_constants.ACTIVE

        return filters

    def post_get(self, request):
        mask_fields = []

        # for record in self.records:
        #     for mask_field in mask_fields:
        #         if mask_field in record:
        #             record[mask_field] = mask_string(record[mask_field])

        super().post_get(request)

    def build_response(self):
        response = super().build_response()
        # response['detail']['user'] = 'hello'
        return response

