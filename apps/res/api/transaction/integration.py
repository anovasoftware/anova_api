from decimal import Decimal

from apps.res.api.transaction.base import AuthorizedTransactionAPIView
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants, status_constants, guest_constants, process_constants

from apps.res.models import Transaction, TransactionItem
from apps.base.models import Item
from apps.static.models import Currency, Type
from core.api_views.api_params import param_spec_to_openapi, PARAM_DEFINITIONS

from core.utilities.api_docs_utilties import params_for
from core.utilities.api_docs_utilties import build_docs_response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter, OpenApiExample


##### CREATE ENTRY IN urls_docs.py ####
# http://localhost:8000/api/v1/integration/transaction/?hotelPublicKey=NC9DXY&typeId=00N&guestId=0004HT&amount=30.00&shape=flat&currencyCode=usd&itemDescription=1GB INTERNET VOUCHER&externalReference=REF00017&externalAuthorizationCode=
class IntegrationTransactionAPIView(AuthorizedTransactionAPIView):
    http_method_names = ['post', 'options', 'head']
    process_id = process_constants.INTEGRATION_TRANSACTION
    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES + (
        'statusId',
        'guestId',
        'typeId',
        'externalReference',
        'externalAuthorizationCode',
        'amount',
        'transactionType'
    )
    PARAM_OVERRIDES = {
        'statusId': dict(required_get=True, allowed=(status_constants.QUEUED,)),
        'guestId': dict(required_post=True, ),
        'amount': dict(required_post=True, ),
        'typeId': dict(
            # required_patch=False,
            allowed=(
                type_constants.RES_TRANSACTION_STAGED_CHARGE,
                type_constants.RES_TRANSACTION_STAGED_REFUND,
                type_constants.RES_TRANSACTION_STAGED
            )
        ),
        'externalReference': dict(required_post=True, ),
    }

    DOC_CONTEXT = {}
    RECORD_DICT = {
        'transaction_id': {'description': 'Transaction id', 'example': '00912211'},
        'description': {'description': 'Description of transaction.', 'example': '1GB INTERNET VOUCHER'},
        'guest_id': {'description': 'Guest id.', 'example': '002149'},
        'event_id': {'description': 'Event id.', 'example': '009112'},
        'currency_id': {'description': 'Currency', 'example': '002'},
        # 'item_id': {'description': 'POS Item Id', 'example': '0100091'}
    }
    DOC_PARAMETERS = [
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
        # OpenApiParameter(
        #     name='transactionType',
        #     type=OpenApiTypes.STR,
        #     location='query',
        #     required=True,
        #     description='Transaction type (CHARGE, REFUND).'
        # ),
        param_spec_to_openapi(
            PARAM_DEFINITIONS['transactionType'],
            method='POST',
        ),

    ]
    DOC_PARAMETER_OVERRIDES = {
        'guestId': {'required': True},
        'typeId': {'exclude': True},
    }
    DOC_GET_ONLY_PARAMETERS = []
    DOC_POST_ONLY_PARAMETERS = ['amount', 'currencyCode', ]
    DOC_POST_SUMMARY = 'Post a charge or refund to a guest.'
    DOC_POST_DESCRIPTION = 'Post a charge or refund to a guest.'
    DOC_TAGS = ['Transaction']
    DOC_EXAMPLE_NAME = 'TransactionSuccess'

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
            get=extend_schema(exclude=True),
            post=extend_schema(
                summary=cls.DOC_POST_SUMMARY,
                description=cls.DOC_POST_DESCRIPTION,
                tags=cls.DOC_TAGS,
                parameters=params_for(
                    method='POST',
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
        )

    def __init__(self):
        super().__init__()
        self.item_id = None
        self.item_description = None
        self.amount = 0.00
        self.currency_code = None
        self.item = None
        self.external_reference = None
        self.external_authorization_code = None
        self.transaction_type = None
        self.transaction = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

        if self.is_post():
            if self.success:
                type_key = f'RES_TRANSACTION_STAGED_{self.transaction_type}'
                type_obj = Type.objects.filter(type_key=type_key).first()
                if not type_obj:
                    self.set_message(f'invalid transactionType={self.transaction_type}.',
                                     http_status_id=status_constants.HTTP_BAD_REQUEST)
                else:
                    self.type_id = type_obj.pk

            self.set_currency_id()
            self.set_item_id()

    def load_models(self, request):
        super().load_models(request)

        # self.load_status(self.status_id)
        if self.is_post():
            self.item = Item.objects.get(pk=self.item_id)

    # def validate(self, request):
    #     super().validate(request)

    def _get(self, request):
        super()._get(request)

        if self.success:
            transaction_ids = {record.get('transaction_id') for record in self.records if record.get('transaction_id')}

            transaction_items = TransactionItem.objects.filter(
                transaction_id__in=transaction_ids,
                status_id=status_constants.ACTIVE
            ).values(
                'transaction_item_id',
                'transaction_id',
                'item_id',
                'item__description',
                'quantity',
                'price',
            )

            external_mappings = {
                'guest_id': {'app_name': 'res', 'model_name': 'Guest'},
                'event_id': {'app_name': 'res', 'model_name': 'Event'},
                'currency_id': {'app_name': 'static', 'model_name': 'Currency'},
            }

            for key, value in external_mappings.items():
                field_name = f'external_{key}'
                app_name = value['app_name']
                model_name = value['model_name']
                self.add_external_mapping_to_records(
                    field_name,
                    key,
                    app_name=app_name,
                    model_name=model_name,
                    records=self.records
                )

            for record in self.records:
                transaction_id = record['transaction_id']

                record['transaction_items'] = []
                for transaction_item in transaction_items.filter(transaction_id=transaction_id):
                    record['transaction_items'].append(
                        {
                            'transaction_item_id': transaction_item['transaction_item_id'],
                            'transaction_id': transaction_item['transaction_id'],
                            'item_id': transaction_item['item_id'],
                            'description': transaction_item['item__description'],
                            'quantity': transaction_item['quantity'],
                            'price': transaction_item['price'],
                        }
                    )
                self.add_external_mapping_to_records(
                    field_name='external_item_id',
                    from_field_name='item_id',
                    app_name='base',
                    model_name='Item',
                    records=record['transaction_items']
                )

    def validate_post(self, request):
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
        value_list = list(self.RECORD_DICT.keys())
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['status_id'] = self.status_id
        filters['event_id'] = self.hotel_extension.current_event_id
        return filters

    def validate_request(self, request):
        pass

    def _get_record(self, request):
        record = super()._get_record(request)
        record = record | {
            'type_id': self.type_id,
            'status_id': status_constants.TRANSACTION_QUEUED,
            'event_id': self.hotel_extension.current_event_id,
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

        self.records_created += 1
        self.data['transaction_id'] = transaction.transaction_id

    def build_response(self):
        response = super().build_response()

        # if self.currency_id:
        #     response['context']['currencyId'] = self.currency_id
        #     response['context']['currencyCode'] = self.currency_code
        #
        # if self.item_id:
        #     response['context']['itemId'] = self.item_id
        #     response['context']['itemDescription'] = self.item_description

        # if self.item:
        #     item = self.item
        #     response['context']['item'] = {
        #         'item_id': item.item_id,
        #         'description': item.description
        #     }

        # if self.transaction:
        #     response['data']['transactionId'] = self.transaction.transaction_id
        return response


IntegrationTransactionAPIView = IntegrationTransactionAPIView.get_schema()(IntegrationTransactionAPIView)
