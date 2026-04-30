from django.db.models import QuerySet

from apps.base.models import Item, RoleItem, UserRole
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import process_constants, status_constants
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.utilities.api_docs_utilties import params_for, build_docs_response


class IntegrationPosMenuItemListAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.INTEGRATION_POS_MENU_ITEM_LIST
    http_method_names = ['get', 'options', 'head']

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES
    DOC_CONTEXT = {}

    RECORD_DICT = {
        'item__item_id': {'description': 'Item identifier.', 'example': 'A00001'},
        'item__code': {'description': 'Item code.', 'example': 'BEER'},
        'item__description': {'description': 'Item description.', 'example': 'Beer'},
        'item__category__category_id': {'description': 'Category identifier.', 'example': 'A0001'},
        'item__category__description': {'description': 'Category description.', 'example': 'Beverages'},
        # 'pos_menu__pos_menu_id': {'description': 'Menu identifier.', 'example': '000001'},
        # 'pos_menu__category__description': {'description': 'Menu description.', 'example': 'Lunch'},
        'price': {'description': 'Item price.', 'example': '1.29'},
    }

    DOC_PARAMETERS = []
    DOC_PARAMETER_OVERRIDES = {
        'guestId': {'exclude': True},
        'typeId': {'exclude': True},
    }
    DOC_GET_ONLY_PARAMETERS = []
    DOC_POST_ONLY_PARAMETERS = []

    DOC_GET_SUMMARY = 'Retrieve items available to user based on roles'
    DOC_GET_DESCRIPTION = 'Returns items that the authenticated user is allowed to access via role mappings.'
    DOC_TAGS = ['Item']
    DOC_EXAMPLE_NAME = 'ItemSuccess'

    @classmethod
    def get_schema(cls):
        parameters = cls.get_doc_parameters()
        get_only_parameters = cls.get_doc_get_only_parameters()
        post_only_parameters = cls.get_doc_post_only_parameters()
        context = cls.get_doc_context()

        _, _, response_envelope, docs_example = build_docs_response(
            record_dict=cls.RECORD_DICT,
            context=context,
            parameters=parameters,
        )

        return extend_schema_view(
            get=extend_schema(
                summary=cls.DOC_GET_SUMMARY,
                description=cls.DOC_GET_DESCRIPTION,
                tags=cls.DOC_TAGS,
                parameters=params_for(
                    method='GET',
                    parameters=parameters,
                    post_only=post_only_parameters,
                    get_only=get_only_parameters
                ),
                responses={200: response_envelope},
                examples=[
                    OpenApiExample(
                        cls.DOC_EXAMPLE_NAME,
                        value=docs_example,
                    )
                ]
            ),
            post=extend_schema(exclude=True),
        )

    def __init__(self):
        super().__init__()
        self.items: QuerySet[Item] = Item.objects.none()
        self.app_name = 'base'
        self.model_name = 'PosMenuItem'
        self.hotel_id_field = 'pos_menu__hotel_id'

    def load_models(self, request, *args, **kwargs):
        super().load_models(request)

        if self.success:
            user_role_ids = UserRole.objects.filter(
                user_id=self.user.user_id,
                effective_status__status_id=status_constants.EFFECTIVE_STATUS_CURRENT,
            ).values_list('role_id', flat=True)

            item_ids = RoleItem.objects.filter(
                role_id__in=user_role_ids,
                status__status_id=status_constants.ACTIVE,
                allow_api_charge=True,
            ).values_list('item_id', flat=True)

            self.items = Item.objects.filter(
                item_id__in=item_ids,
                effective_status_id=status_constants.EFFECTIVE_STATUS_CURRENT,
                status__status_id=status_constants.ACTIVE,
            ).distinct()

    def get_value_list(self):
        return list(self.RECORD_DICT.keys())

    def get_query_filter(self):
        filters = super().get_query_filter()
        item_ids = self.items.values_list('pk', flat=True)
        filters['item_id__in'] = item_ids
        filters['pos_menu__effective_status_id'] = status_constants.EFFECTIVE_STATUS_CURRENT
        return filters


IntegrationPosMenuItemListAPIView = IntegrationPosMenuItemListAPIView.get_schema()(IntegrationPosMenuItemListAPIView)