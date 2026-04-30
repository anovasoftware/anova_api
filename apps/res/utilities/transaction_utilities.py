from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from apps.res.models import Transaction, TransactionItem
from constants import status_constants


class TransactionUtilities:
    @staticmethod
    def cleanup_transactions(days_old=7):
        cutoff_date = timezone.now() - timedelta(days=days_old)

        Transaction.objects.annotate(
            item_count=Count('transactionItems')
        ).filter(
            status_id=status_constants.TRANSACTION_QUEUED,
            item_count=0
        ).update(
            status_id=status_constants.TRANSACTION_INVALID,
            internal_comment='No items in transaction.'
        )

        # expired_count = (
        #     Transaction.objects
        #     .filter(
        #         status_id=status_constants.QUEUED,
        #         tstamp__lt=cutoff_date,
        #     )
        #     .update(status_id=status_constants.EXPIRED)
        # )
        #
        # result = {
        #     'noItemCount': no_item_count,
        #     'expiredCount': expired_count,
        # }

        # return result