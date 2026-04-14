from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import status_constants, process_constants

from apps.res.models import Transaction

from django.core.exceptions import ObjectDoesNotExist


class TransactionStatusAPIView(AuthorizedHotelAPIView):
    process_id = process_constants.RES_TRANSACTION_STATUS

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES + ('statusId', )
    PARAM_OVERRIDES = {
        # 'recordId': dict(required_patch=True),
        'statusId': dict(required_patch=True, allowed=(status_constants.TRANSACTION_QUEUED,)),
        'typeId': dict(required_patch=False),
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Transaction'

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def load_models(self, request):
        super().load_models(request)

        try:
            self.record = Transaction.objects.get(pk=self.record_id)
        except ObjectDoesNotExist as e:
            message = f'record_id  not found: {self.record_id}'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def validate(self, request):
        super().validate(request)

        if self.record.status_id != status_constants.QUEUED:
            message = f'id={self.record_id} is not in queued status.'
            self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)

    def _patch(self, request):
        # message = f'change status of id={self.record_id} from {self.record.status_id} to {self.status_id}.'
        # self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
        if self.success:
            self.record.status_id = self.status_id
            self.record.save()
