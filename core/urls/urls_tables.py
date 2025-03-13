from django.urls import path

from apps.res.table_api_views.category_api_views import AuthorizedCategoryAPIView

urlpatterns = [
    path('category/', AuthorizedCategoryAPIView.as_view()),
]
