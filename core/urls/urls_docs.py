from django.urls import path

from apps.res.api.transaction.integration import IntegrationTransactionAPIView
from apps.res.table_api_views.table_guest_api_views import IntegrationGuestAPIView

urlpatterns = [
    path('/api/v1/integration/guest', IntegrationGuestAPIView.as_view()),
    path('api/v1/integration/transaction/', IntegrationTransactionAPIView.as_view()),
    # path('api/v1/table/res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
]
