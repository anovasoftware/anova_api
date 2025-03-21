from django.urls import path

from apps.base.table_api_views.company_api_views import AuthorizedCompanyAPIView
from apps.base.table_api_views.person_api_view import AuthorizedPersonAPIView

from apps.res.table_api_views.category_api_views import AuthorizedCategoryAPIView
from apps.res.table_api_views.room_api_views import AuthorizedRoomAPIView

urlpatterns = [
    path('base/company/', AuthorizedCompanyAPIView.as_view()),
    path('base/person/', AuthorizedPersonAPIView.as_view()),

    path('res/category/', AuthorizedCategoryAPIView.as_view()),
    path('res/room/', AuthorizedRoomAPIView.as_view()),
]
