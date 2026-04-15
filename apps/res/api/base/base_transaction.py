from decimal import Decimal
from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from constants import type_constants, event_constants, status_constants, guest_constants, process_constants

from apps.res.models import Transaction, TransactionItem
from apps.base.models import Item, ExternalMapping
from apps.static.models import Currency

from django.core.exceptions import ObjectDoesNotExist

from core.utilities.api_docs_utilties import params_for
from core.utilities.api_docs_utilties import build_docs_response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter, OpenApiExample


##### I need to "graduate" the IntegrationTransactionAPIView" to AuthorizedTransactionAPIView"
class AuthorizedTransactionAPIView(AuthorizedHotelAPIView):
    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'Transaction'
