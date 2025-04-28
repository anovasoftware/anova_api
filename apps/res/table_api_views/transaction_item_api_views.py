from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


class AuthorizedTransactionItemAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'TransactionItem'
        self.accepted_type_ids = [
            type_constants.RES_TRANSACTION_ITEM_REGULAR
        ]
        self.hotel_id_field = 'transaction__hotel_id'

    def get_value_list(self):
        value_list = [
            'transaction_item_id',
            # 'description'
        ]
        return value_list
