from decimal import Decimal
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView, context, parameters
from apps.static.table_api_views.hotel_api_views import post_only_parameters, get_only_parameters
from constants import type_constants, event_constants, status_constants, guest_constants, process_constants

from apps.res.models import Transaction, TransactionItem
from apps.base.models import Item
from apps.static.models import Currency

from core.utilities.api_docs_utilties import override_parameters, params_for
from core.utilities.api_docs_utilties import build_docs_response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.openapi import AutoSchema

context = context or {}

record_dict = {
    'transaction_id': {'description': 'Transaction id', 'example': '00912211'},
    'description': {'description': 'Description of transaction.', 'example': '1GB INTERNET VOUCHER'},
    'guest_id': {'description': 'Guest id.', 'example': '002149'}
}
parameters = override_parameters(parameters, 'guestId', required=True)

parameters = parameters + [
    OpenApiParameter(
        name='amount',
        type=OpenApiTypes.NUMBER,
        location='query',
        required=True,
        description='Transaction amount (e.g., 7.29).'
    ),
    OpenApiParameter(
        name='currencyCode',
        type=OpenApiTypes.STR,
        location='query',
        required=True,
        description='ISO currency code (e.g., USD).'
    ),
    OpenApiParameter(
        name='externalReference',
        type=OpenApiTypes.STR,
        location='query',
        required=True,
        description='External reference identifier (e.g., R00088).'
    ),
    OpenApiParameter(
        name='externalAuthorizationCode',
        type=OpenApiTypes.STR,
        location='query',
        required=False,
        description='External authorization or approval code.'
    ),
    OpenApiParameter(
        name='itemDescription',
        type=OpenApiTypes.STR,
        location='query',
        required=True,
        description='Description of item or service (e.g., 1GB INTERNET VOUCHER).'
    ),
]
get_only_parameters = get_only_parameters + []
post_only_parameters = post_only_parameters + ['amount', 'currencyCode', ]

record_dict, record_serializer, response_envelope, docs_example = build_docs_response(
    record_dict=record_dict,
    context=context,
    parameters=parameters,
)

@extend_schema_view(
    get=extend_schema(exclude=True),
    post=extend_schema(
        summary='Post a charge or refund to a guest.',
        description='Post a charge or refund to a guest.',
        tags=['Transaction'],
        parameters=params_for(
            method='POST',
            parameters=parameters,
            post_only=post_only_parameters,
            get_only=get_only_parameters
        ),
        responses={200: response_envelope},
        examples=[
            OpenApiExample(
                'TransactionSuccess',
                value=docs_example,  # <-- YOUR full envelope example here
            )
        ]
    ),
)
##### CREATE ENTRY IN urls_docs.py ####
class AuthorizedTransactionAPIView(AuthorizedHotelAPIView):
    schema = AutoSchema()
    process_id = process_constants.RES_TRANSACTION

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Transaction'
        self.accepted_type_ids = [
            type_constants.RES_TRANSACTION_STAGED_SALE,
            type_constants.RES_TRANSACTION_STAGED_REFUND,
            # type_constants.RES_TRANSACTION_SALE,
            # type_constants.RES_TRANSACTION_PAYMENT
        ]
        self.item_id = None
        self.item_description = None
        self.amount = 0.00
        self.currency_code = None
        self.item = None
        self.external_reference = None
        self.external_authorization_code = None
        self.transaction = None

    def load_request(self, request):
        self.guest_id_required = self.is_post()
        super().load_request(request)

        if request.method == 'POST':
            # self.guest_id = self.get_param('guestId', None, True)
            self.external_reference = self.get_param('externalReference', None, True)
            self.external_authorization_code = self.get_param('externalAuthorizationCode', '')

            if self.posting_type and self.posting_type in ['simple', ]:
                self.json_required = False

                self.amount = self.get_param('amount', None, True, parameter_type='decimal')
                self.set_currency_id()
                self.set_item_id()

    def load_models(self, request):
        super().load_models(request)
        self.item = Item.objects.get(pk=self.item_id)

    def validate(self, request):
        super().validate(request)
        if not self.guest.authorized_to_charge_flag == 'Y':
            message = f'guest_id={self.guest_id} not authorized to charge.'
            self.add_message(message, http_status_id=status_constants.HTTP_UNAUTHORIZED)
        if self.success and Transaction.objects.filter(external_reference=self.external_reference).exists():
            message = f'externalReference={self.external_reference} already exists.'
            self.set_message(message, http_status_id=status_constants.HTTP_FORBIDDEN)


    def set_currency_id(self):
        self.currency_code = self.get_param('currencyCode', None, False)
        self.currency_id = self.get_param('currencyId', None, False)

        if not self.currency_id and not self.currency_code:
            message = 'currencyId or currencyCode not supplied.'
            self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif self.currency_id and self.currency_code:
            message = 'currencyId and currencyCode supplied. only one is allowed.'
            self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif self.currency_id:
            currencies = Currency.objects.filter(pk=self.currency_id)
            if currencies.count() == 0:
                message = f'invalid currencyId={self.currency_id}.'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            else:
                self.currency_code = currencies[0].code
        elif self.currency_code:
            self.currency_code = self.currency_code.upper()
            currencies = Currency.objects.filter(code=self.currency_code)
            if currencies.count() == 0:
                message = f'invalid currencyCode={self.currency_code}.'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            else:
                self.currency_id = currencies[0].pk

    def set_item_id(self):
        self.item_id = self.get_param('itemId', None, False)
        self.item_description = self.get_param('itemDescription', None, False)

        if not self.item_id and not self.item_description:
            message = 'itemId or itemDescription not supplied.'
            self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif self.item_id and self.item_description:
            message = 'itemId and itemDescription supplied. only one is allowed.'
            self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        elif self.item_id:
            items = Item.objects.filter(pk=self.item_id)
            if items.count() == 0:
                message = f'invalid itemId={self.item_id}.'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            else:
                self.item_description = items[0].description
        elif self.item_description:
            self.item_description = self.item_description.strip()
            items = Item.objects.filter(description__iexact=self.item_description)
            count = items.count()

            if count == 0:
                message = f'invalid itemDescription={self.item_description}.'
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            elif count > 1:
                message = (
                    f'multiple items match itemDescription={self.item_description}. '
                    'please specify itemId instead.'
                )
                self.add_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
            else:
                self.item_id = items[0].pk

    def get_value_list(self):
        value_list = list(record_dict.keys())
        # value_list = [
        #     'transaction_id',
        #     'description',
        #     'guest_id'
        #     # 'status__status_id',
        #     # 'status__description',
        #     # 'transactionItems'
        # ]
        return value_list

    # def _post_simple(self, request):
    #     hotel_type = self.hotel_type
    #     hotel_items = HotelItem.objects.filter(
    #         hotel_id=self.hotel_id,
    #         special_item_type_id=hotel_type.type_id
    #     )
    #     if hotel_items.count() == 1:
    #         hotel_item = hotel_items[0]
    #         self.item = Item.objects.get(pk=hotel_item.item_id)
    #         self._post_simple_save(request)
    #     else:
    #         self.set_message(f'unable to find item associated with itemKey: {self.item_key}')
    #
    #     self.set_message('under construction', http_status_id=status_constants.HTTP_BAD_REQUEST)

    def validate_request(self, request):
        pass

    def _get_record(self, request):
        record = super()._get_record(request)
        record = record | {
            'type_id': self.type_id,
            'status_id': status_constants.QUEUED,
            'event_id': event_constants.TO_BE_ANNOUNCED,
            'guest_id': self.guest_id,
            'server_guest_id': guest_constants.NOT_APPLICABLE,
            'description': self.item_description,
            'external_reference': self.external_reference,
            'external_authorization_code': self.external_authorization_code,
        }

        return record

    def _post_simple(self, request):
        record = self._get_record(request)
        transaction = Transaction.objects.create(**record)

        record_item = {
            'transaction_id': transaction.transaction_id,
            'item_id': self.item.item_id,
            'type_id': type_constants.RES_TRANSACTION_ITEM_REGULAR,
            'status_id': status_constants.ACTIVE,
            'description': self.item.description,
            'quantity': Decimal(1.00),
            'price': self.amount
        }
        self.transaction = transaction
        transaction_item = TransactionItem.objects.create(**record_item)

        fields = self.get_value_list()
        self.records = list(Transaction.objects.filter(pk=transaction.transaction_id).values(*fields))

    def build_response(self):
        response = super().build_response()

        if self.currency_id:
            response['context']['currencyId'] = self.currency_id
            response['context']['currencyCode'] = self.currency_code

        if self.item_id:
            response['context']['itemId'] = self.item_id
            response['context']['itemDescription'] = self.item_description

        # if self.item:
        #     item = self.item
        #     response['context']['item'] = {
        #         'item_id': item.item_id,
        #         'description': item.description
        #     }

        # if self.transaction:
        #     response['data']['transactionId'] = self.transaction.transaction_id
        return response


# def get_currency_id(currency: str):
#     currency_id = None
#     currencies =Currency.objects.filter(
#             Q(currency_id=currency) | Q(code=currency)
#         )
#     if currencies.count() == 1:
#         currency_id = currencies[0].currency_id
#
#     return currency_id