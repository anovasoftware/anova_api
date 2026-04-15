from django.urls import path

from apps.res.api.integration.transaction import IntegrationTransactionCreateAPIView
from apps.res.api.integration.guest import IntegrationGuestListAPIView

urlpatterns = [
    path('/api/v1/integration/guests/', IntegrationGuestListAPIView.as_view()),
    path('api/v1/integration/transactions/', IntegrationTransactionCreateAPIView.as_view()),
    # path('api/v1/table/res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
]
