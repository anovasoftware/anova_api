from django.urls import path

from apps.res.table_api_views.guest_room_api_views import AuthorizedGuestRoomAPIView

urlpatterns = [
    path('api/v1/table/res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
]
