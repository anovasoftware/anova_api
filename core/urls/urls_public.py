from django.contrib import admin
from django.urls import path
from core.api_views.core_api import TestAPI
from apps.base.table_api_views.user_api_views import PublicUserAPIView
from django.urls import path, include
from core.api_views.core_api import health_check


urlpatterns = [
    path("health/", health_check),
    path('test-api/', TestAPI.as_view(), name='test-api'),

    path('table/base/user/', PublicUserAPIView.as_view(), name='PublicUserAPIView'),

]

