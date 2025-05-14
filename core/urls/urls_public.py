from django.contrib import admin
from django.urls import path
from core.api_views.core_api import TestAPI, GuestRoomAPI
from django.urls import path, include

urlpatterns = [
    path('test-api/', TestAPI.as_view(), name='test-api'),
]

