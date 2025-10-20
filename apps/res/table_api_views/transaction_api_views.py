from decimal import Decimal
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants, event_constants, status_constants, guest_constants
from apps.res.models import Guest, HotelItem, Transaction, TransactionItem
from apps.base.models import Category, Item
from apps.static.models import Type


# http://api.anovasea.net/api/v1/external/res/charge?room=<room>&amount=<amount>&guestId=<guestId>
class AuthorizedTransactionAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Transaction'
        self.accepted_type_ids = [
            type_constants.RES_TRANSACTION_STAGED_SALE,
            type_constants.RES_TRANSACTION_SALE,
            type_constants.RES_TRANSACTION_PAYMENT
        ]
        self.hotel_type = None
        self.room_code = None
        self.item_key = None
        self.amount = 0.00
        self.item = None

    def load_request(self, request):
        super().load_request(request)

        self.posting_type = self.get_param('postingType', None, True)

        if self.posting_type in ['simple', ]:
            self.json_required = False

            self.guest_id = self.get_param('guestId', None, True)
            self.item_key = self.get_param('itemKey', None, True)
            self.amount = self.get_param('amount', None, True, parameter_type='decimal')

            if self.success:
                special_item_type_id = f'RES_HOTEL_ITEM_SPECIAL_ITEM_{self.item_key}'
                if Type.objects.filter(type_key=special_item_type_id).exists():
                    self.hotel_type = Type.objects.get(type_key=special_item_type_id)
                else:
                    self.set_message(f'invalid itemKey={self.item_key}.', success=False)

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

        self.set_message('under construction', success=False)

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

        if self.item:
            item = self.item
            response['context']['item'] = {
                'item_id': item.item_id,
                'description': item.description
            }
        return response

