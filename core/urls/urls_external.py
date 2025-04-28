from django.urls import path

from apps.res.table_api_views.guest_room_api_views import AuthorizedGuestRoomAPIView

urlpatterns = [
    path('res/guest_room/', AuthorizedGuestRoomAPIView.as_view(), kwargs={'thirdPartyFlag': 'Y'}),  # kwargs not working
]
