from django.urls import path, include

from apps.base.api_views_forms.form_001 import Form001APIView

urlpatterns = [
    path('form_data/001', Form001APIView.as_view()),
]

