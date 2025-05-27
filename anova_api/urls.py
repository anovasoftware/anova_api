from django.contrib import admin
from django.urls import path
from core.api_views.core_api import TestAPI, GuestRoomAPI
from django.urls import path, include

urlpatterns = [
    path('api/v1/public/', include('core.urls.urls_public')),
    path('admin/', admin.site.urls),
    path('record/guest_room/', GuestRoomAPI.as_view(), name='guest-room'),

    path('api/v1/table/', include('core.urls.urls_tables')),
    path('api/v1/external/', include('core.urls.urls_tables')),
]
# https://yourPMS/GetRoomGuests?room=123&hotelId=xxxyy

