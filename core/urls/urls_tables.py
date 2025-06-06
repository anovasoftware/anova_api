from django.urls import path

from apps.base.table_api_views.category_api_views import AuthorizedCategoryAPIView
from apps.base.table_api_views.chart_field_api_views import AuthorizedChartFieldAPIView
from apps.base.table_api_views.email_api_views import AuthorizedEmailAPIView
from apps.base.table_api_views.company_api_views import AuthorizedCompanyAPIView
from apps.base.table_api_views.hotel_type_api_views import AuthorizedHotelTypeAPIView
from apps.base.table_api_views.item_api_views import AuthorizedItemAPIView
from apps.base.table_api_views.person_api_view import AuthorizedPersonAPIView
from apps.base.table_api_views.pos_menu_api_views import AuthorizedPosMenuAPIView
from apps.base.table_api_views.pos_menu_item_api_views import AuthorizedPosMenuItemAPIView

from apps.res.table_api_views.guest_api_views import AuthorizedGuestAPIView
from apps.res.table_api_views.guest_room_api_views import AuthorizedGuestRoomAPIView
from apps.res.table_api_views.hotel_item_api_views import AuthorizedHotelItemAPIView
from apps.res.table_api_views.event_api_views import AuthorizedEventAPIView
from apps.res.table_api_views.room_api_views import AuthorizedRoomAPIView
from apps.res.table_api_views.reservation_api_views import AuthorizedReservationAPIView
from apps.res.table_api_views.transaction_api_views import AuthorizedTransactionAPIView
from apps.res.table_api_views.transaction_item_api_views import AuthorizedTransactionItemAPIView

urlpatterns = [
    path('base/category/', AuthorizedCategoryAPIView.as_view()),
    path('base/chart_field/', AuthorizedChartFieldAPIView.as_view()),
    path('base/company/', AuthorizedCompanyAPIView.as_view()),
    path('base/email/', AuthorizedEmailAPIView.as_view()),
    path('base/hotel_type/', AuthorizedHotelTypeAPIView.as_view()),
    path('base/item/', AuthorizedItemAPIView.as_view()),
    path('base/person/', AuthorizedPersonAPIView.as_view()),
    path('base/pos_menu/', AuthorizedPosMenuAPIView.as_view()),
    path('base/pos_menu_item/', AuthorizedPosMenuItemAPIView.as_view()),

    path('res/event/', AuthorizedEventAPIView.as_view()),
    path('res/guest/', AuthorizedGuestAPIView.as_view()),
    path('res/guest_room/', AuthorizedGuestRoomAPIView.as_view()),
    path('res/hotel_item/', AuthorizedHotelItemAPIView.as_view()),
    path('res/reservation/', AuthorizedReservationAPIView.as_view()),
    path('res/room/', AuthorizedRoomAPIView.as_view()),
    path('res/transaction/', AuthorizedTransactionAPIView.as_view()),
    path('res/transaction_item/', AuthorizedTransactionItemAPIView.as_view()),
]
