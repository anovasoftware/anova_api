from django.contrib import admin
from django.urls import path
from core.api_views.core_api import GuestRoomAPI
from django.urls import path, include
from core.api_views.core_api import health_check
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import JsonResponse
from constants import  constants
# urls.py

def ping(request):
    return JsonResponse({'status': 'OK', 'message': f'API connection successful version={constants.VERSION}'})


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('ping/', ping, name='ping'),
    path("health/", health_check),
    path('api/v1/public/', include('core.urls.urls_public')),
    path('admin/', admin.site.urls),
    path('record/guest_room/', GuestRoomAPI.as_view(), name='guest-room'),

    path('api/v1/form/', include('core.urls.urls_forms')),
    path('api/v1/table/', include('core.urls.urls_tables')),
    # path('api/v1/external/', include('core.urls.urls_tables')),

    # --- NEW: schema + docs ---
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("api/schema/", SpectacularAPIView.as_view(urlconf="core.urls.urls_docs"), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# https://yourPMS/GetRoomGuests?room=123&hotelId=xxxyy


