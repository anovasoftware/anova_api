from core.api_views.table_api_views import PublicTableAPIView
from apps.static.models import Menu
from constants import type_constants, status_constants, process_constants


class PublicMenuAPIView(PublicTableAPIView):
    process_id = None

    PARAM_NAMES = PublicTableAPIView.PARAM_NAMES
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
        self.order_by = ('order_by',)
        # self.accepted_type_ids = [
        #     'ALL'
        #     # type_constants.MENU_HEADER_BAR
        # ]

        self.user = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

        # if self.menu_id:
        #     try:
        #         self.menu = Menu.objects.filter(type_id=self.type_id)
        #     except Exception as e:
        #         self.set_message(f'room not found: {self.user_id}', success=False)

    def get_value_list(self):
        value_list = [
            'menu_id',
            'parent_menu_id',
            'type_id',
            'grid_id',
            'description',
            'title',
            'sub_title',
            'breadcrumb_name',
            'route',
            'page__page_id',
            'page__description',
            'icon',
            'hotel_required'
        ]

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['status_id'] = status_constants.ACTIVE

        return filters

    def post_get(self, request):
        mask_fields = []
        if self.hotel.type_id == type_constants.HOTEL_HOTEL:
            room_or_cabin = 'Room'
        else:
            room_or_cabin = 'Cabin'

        for record in self.records:
            for key, value in record.items():
                if isinstance(value, str):
                    record[key] = (
                        value
                        .replace('<<HOTEL>>', self.hotel.description)
                        .replace('<<PROPERTY>>', self.hotel.type.description)
                        .replace('<<ROOM>>', room_or_cabin)
                    )

        # for record in self.records:
        #     for mask_field in mask_fields:
        #         if mask_field in record:
        #             record[mask_field] = mask_string(record[mask_field])

        super().post_get(request)

    def build_response(self):
        response = super().build_response()
        # response['detail']['user'] = 'hello'
        return response
