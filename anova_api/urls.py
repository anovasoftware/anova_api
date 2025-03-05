from django.contrib import admin
from django.urls import path
from core.core_api import TestAPI, GuestRoomAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-api/', TestAPI.as_view(), name='test-api'),
    path('record/guest_room/', GuestRoomAPI.as_view(), name='guest-room'),
]
# https://yourPMS/GetRoomGuests?room=123&hotelId=xxxyy