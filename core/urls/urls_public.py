from django.contrib import admin
from django.urls import path
from core.api_views.core_api import TestAPI
from django.urls import path, include

from apps.static.table_api_views.form_api_views import PublicFormAPIView
from apps.static.table_api_views.menu_api_views import PublicMenuAPIView
from apps.base.table_api_views.user_api_views import PublicUserAPIView
from django.http import JsonResponse

def ping(request):
    return JsonResponse({'status': 'OK', 'message': 'API connection successful'})


urlpatterns = [
    path('ping/', ping, name='ping'),
    path('test-api/', TestAPI.as_view(), name='test-api'),

    path('table/base/user/', PublicUserAPIView.as_view(), name='PublicUserAPIView'),

    path('table/static/form/', PublicFormAPIView.as_view(), name='PublicFormAPIView'),
    path('table/static/menu/', PublicMenuAPIView.as_view(), name='PublicMenuAPIView'),
]

