from apps.static.table_api_views.form_api_views import PublicFormAPIView
from apps.base.models import EventLog
from constants import  form_constants


class Form001APIView(PublicFormAPIView):
    form_id = form_constants.LOGIN
    base_model = EventLog

    def __init__(self):
        super().__init__()

