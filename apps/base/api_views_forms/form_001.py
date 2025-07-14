from apps.static.table_api_views.form_api_views import PublicFormAPIView
from apps.base.models import EventLog
from constants import form_constants, page_constants
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.base.serializers.user import UserSerializer


class Form001APIView(PublicFormAPIView):
    form_id = form_constants.LOGIN
    base_model = EventLog

    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None

    def pre_post(self, request):
        record = request.data

        self.username = record['string01']
        self.password = record['string02']

        record['string02'] = '#' * len(self.password)

        self.record = record

    def post_post(self, request):
        super().post_post(request)

        # TODO: here is where I will authenticate my user
        user = authenticate(username=self.username, password=self.password)

        if user:
            refresh = RefreshToken.for_user(user)
            self.data['refresh'] = str(refresh)
            self.data['access'] = str(refresh.access_token)
            self.data['redirect'] = f'navigator/{page_constants.HOME}'
            self.data['user'] = UserSerializer(user).data
        else:
            self.set_message(
                message='Invalid username or password',
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
