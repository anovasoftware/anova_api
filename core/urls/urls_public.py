from django.contrib import admin
from django.urls import path
from core.api_views.core_api import TestAPI
from django.urls import path, include

from apps.base.table_api_views.user_api_views import PublicUserAPIView
from apps.static.table_api_views.menu_api_views import PublicMenuAPIView


urlpatterns = [
    path('test-api/', TestAPI.as_view(), name='test-api'),

    path('table/base/user/', PublicUserAPIView.as_view(), name='PublicUserAPIView'),

    path('table/static/menu/', PublicMenuAPIView.as_view(), name='PublicMenuAPIView'),
]

