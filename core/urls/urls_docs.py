from django.urls import path

from apps.res.table_api_views.guest_room_api_views import AuthorizedGuestRoomAPIView
from apps.res.table_api_views.transaction_api_views import AuthorizedTransactionAPIView
from apps.res.table_api_views.table_guest_api_views import IntegrationGuestAPIView

urlpatterns = [
    path('/api/v1/integration/guest', IntegrationGuestAPIView.as_view()),

    # path('api/v1/table/res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
    path('api/v1/table/res/transaction/', AuthorizedTransactionAPIView.as_view()),
]
