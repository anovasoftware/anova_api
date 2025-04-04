from django.urls import path

from apps.base.table_api_views.company_api_views import AuthorizedCompanyAPIView
from apps.base.table_api_views.person_api_view import AuthorizedPersonAPIView

from apps.res.table_api_views.category_api_views import AuthorizedCategoryAPIView
from apps.res.table_api_views.guest_api_views import AuthorizedGuestAPIView
from apps.res.table_api_views.guest_room_api_views import AuthorizedGuestRoomAPIView
from apps.res.table_api_views.room_api_views import AuthorizedRoomAPIView
from apps.res.table_api_views.reservation_api_views import AuthorizedReservationAPIView

urlpatterns = [
    path('base/company/', AuthorizedCompanyAPIView.as_view()),
    path('base/person/', AuthorizedPersonAPIView.as_view()),

    path('res/category/', AuthorizedCategoryAPIView.as_view()),
    path('res/guest/', AuthorizedGuestAPIView.as_view()),
    path('res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
    path('res/reservation/', AuthorizedReservationAPIView.as_view()),
    path('res/room/', AuthorizedRoomAPIView.as_view()),
]
