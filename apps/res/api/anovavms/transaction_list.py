from apps.res.api.base.base_transaction import AuthorizedTransactionAPIView
from constants import status_constants, process_constants

from apps.res.models import TransactionItem
from django.db.models import Count


class AnovaVMSTransactionListAPIView(AuthorizedTransactionAPIView):
    http_method_names = ['get', 'options', 'head']
    process_id = process_constants.ANOVAVMS_TRANSACTION_LIST
    PARAM_NAMES = AuthorizedTransactionAPIView.PARAM_NAMES + ('statusId',)
    PARAM_OVERRIDES = {
        'statusId': dict(required_get=True, allowed=(status_constants.TRANSACTION_QUEUED,)),
    }

    RECORD_DICT = {
        'transaction_id': {'description': 'Transaction id', 'example': '00912211'},
        'description': {'description': 'Description of transaction.', 'example': '1GB INTERNET VOUCHER'},
        # 'description_extension': {'description': 'Description extension.', 'example': ''},
        'guest_id': {'description': 'Guest id.', 'example': '002149'},
        'event_id': {'description': 'Event id.', 'example': '009112'},
        'currency_id': {'description': 'Currency', 'example': '002'},
        'status__status_id': {'description': 'Status id.', 'example': '001'},
        'status__description': {'description': 'Status description.', 'example': '001'},
        'transactionItems': {'description': 'Transaction items.', 'example': '[]'},
    }

    def __init__(self):
        super().__init__()
        # self.status_id = status_constants.TRANSACTION_QUEUED

    def _get(self, request):
        super()._get(request)
        self.expand_record_with_external_ids('res', 'Guest', 'guest_id')
        self.expand_record_with_external_ids('res', 'Event', 'event_id')
        self.expand_record_with_external_ids('static', 'Currency', 'currency_id')

        for record in self.records:
            transaction_id = record['transaction_id']
            transaction_items = TransactionItem.objects.filter(transaction_id=transaction_id).values(
                'transaction_item_id',
                'transaction_id',
                'item__category__parent_category_id',
                'item_id',
                'item__item_id',
                'item__description',
                'description_extension',
                'quantity',
                'price',
            )
            transaction_items = list(transaction_items)
            menu_category_id = None
            for transaction_item in transaction_items:
                self.add_external_id(transaction_item, 'base', 'Item', 'item_id')
                if not menu_category_id:
                    menu_category_id = transaction_item['item__category__parent_category_id']
                    record['menu_category_id'] = menu_category_id
                    self.add_external_id(
                        record,
                        'base',
                        'Category',
                        'menu_category_id'
                    )

            record['transaction_items'] = transaction_items

    def get_annotations(self):
        annotations = super().get_annotations()

        annotations['item_count'] = Count('transactionItems')
        return annotations

    def get_value_list(self):
        value_list = list(self.RECORD_DICT.keys())
        return value_list

    def get_query_filter(self):
        filters = super().get_query_filter()
        filters['status_id'] = self.status_id
        filters['item_count__gt'] = 0
        return filters
