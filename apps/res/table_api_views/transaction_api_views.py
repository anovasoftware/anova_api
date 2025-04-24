from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView

from constants import type_constants


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

    def get_value_list(self):
        value_list = [
            'transaction_id',
            'description'
        ]
        return value_list
