from django.urls import path, include

from apps.base.api_views_forms.form_001 import Form001APIView
from apps.base.api_views_forms.form_002 import Form002APIView
# from apps.base.api_views_forms.form_004 import Form004APIView

urlpatterns = [
    path('form_data/001', Form001APIView.as_view()),
    path('form_data/002', Form002APIView.as_view()),
    # path('form_data/004', Form004APIView.as_view()),
]

