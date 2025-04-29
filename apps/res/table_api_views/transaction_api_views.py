from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants
from apps.res.models import Guest


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
        self.room_code = None
        self.guest_id = None
        self.item_key = None
        self.amount = 0.00

    def load_request(self, request):
        super().load_request(request)

        self.posting_type = self.get_param('postingType', None, True)

        if self.posting_type in ['simple', ]:
            self.json_required = False

            self.guest_id = self.get_param('guestId', None, True)
            self.item_key = self.get_param('itemKey', None, True)
            self.amount = self.get_param('amount', None, True, parameter_type='decimal')

    def get_value_list(self):
        value_list = [
            'transaction_id',
            'description',
            'transactionItems'
        ]
        return value_list

    def _post_simple(self, request):
        guest = Guest.objects.get(pk=self.guest_id)
        self.add_message(f'guest={guest.person.last_name}, {guest.person.first_name}')
        self.add_message('under construction', success=False)


