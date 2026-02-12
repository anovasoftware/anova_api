from django.urls import path, include

from apps.base.api_views_forms.form_001 import Form001APIView
from apps.base.api_views_forms.form_002 import Form002APIView

urlpatterns = [
    path('form_data/001', Form001APIView.as_view()),
    path('form_data/002', Form002APIView.as_view()),
]

