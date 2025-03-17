from django.urls import path

from apps.res.table_api_views.category_api_views import AuthorizedCategoryAPIView
from apps.res.table_api_views.room_api_views import AuthorizedRoomAPIView

urlpatterns = [
    path('res/category/', AuthorizedCategoryAPIView.as_view()),
    path('res/room/', AuthorizedRoomAPIView.as_view()),
]
