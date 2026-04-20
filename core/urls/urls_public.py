from core.api_views.core_api import TestAPI
from django.urls import path

from apps.static.table_api_views.form_api_views import PublicFormAPIView
from apps.static.api.tables.menu import PublicMenuAPIView
from apps.base.api.tables.user import PublicUserAPIView


urlpatterns = [
    path('test-api/', TestAPI.as_view(), name='test-api'),

    path('table/base/user/', PublicUserAPIView.as_view(), name='PublicUserAPIView'),

    path('table/static/form/', PublicFormAPIView.as_view(), name='PublicFormAPIView'),
    path('table/static/menu/', PublicMenuAPIView.as_view(), name='PublicMenuAPIView'),
]

