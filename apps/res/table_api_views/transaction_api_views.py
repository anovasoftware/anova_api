from decimal import Decimal
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants, event_constants, status_constants, guest_constants, process_constants
from apps.res.models import Guest, HotelItem, Transaction, TransactionItem
from apps.base.models import Category, Item
from apps.static.models import Type, Currency


class AuthorizedTransactionAPIView(AuthorizedHotelAPIView):
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
        self.hotel_type = None
        self.room_code = None
        self.item_id = None
        self.item_description = None
        self.amount = 0.00
        self.currency_code = None
        self.currency_id = None
        self.item = None

    def load_request(self, request):
        super().load_request(request)

        if request.method == 'POST':
            # self.posting_type = self.get_param('postingType', None, True)
            self.guest_id = self.get_param('guestId', None, True)

            if self.posting_type and self.posting_type in ['simple', ]:
                self.json_required = False

                self.amount = self.get_param('amount', None, True, parameter_type='decimal')
                self.set_currency_id()
                self.set_item_id()

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
        value_list = [
            'transaction_id',
            'description',
            'transactionItems'
        ]
        return value_list

    def _post_simple(self, request):
        hotel_type = self.hotel_type
        hotel_items = HotelItem.objects.filter(
            hotel_id=self.hotel_id,
            special_item_type_id=hotel_type.type_id
        )
        if hotel_items.count() == 1:
            hotel_item = hotel_items[0]
            self.item = Item.objects.get(pk=hotel_item.item_id)
            self._post_simple_save(request)
        else:
            self.set_message(f'unable to find item associated with itemKey: {self.item_key}')

        self.set_message('under construction', http_status_id=status_constants.HTTP_BAD_REQUEST)

    def _post_simple_save(self, request):
        record = {
            'type_id': type_constants.RES_TRANSACTION_STAGED_SALE,
            'status_id': status_constants.QUEUED,
            'hotel_id': self.hotel_id,
            'event_id': event_constants.TO_BE_ANNOUNCED,
            'guest_id': self.guest_id,
            'server_guest_id': guest_constants.NOT_APPLICABLE
        }
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
        transaction_item = TransactionItem.objects.create(**record_item)

    def build_response(self):
        response = super().build_response()

        if self.currency_id:
            response['context']['currencyId'] = self.currency_id
            response['context']['currencyCode'] = self.currency_code

        if self.item_id:
            response['context']['itemId'] = self.item_id
            response['context']['itemDescription'] = self.item_description

        if self.item:
            item = self.item
            response['context']['item'] = {
                'item_id': item.item_id,
                'description': item.description
            }
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