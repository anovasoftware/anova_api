from apps.static.table_api_views.form_api_views import FormParameterAPIView
from constants import form_constants, page_constants, status_constants
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.base.serializers.user import UserSerializer
from apps.base.utilities.user_utilities import get_user_profile

# login form
class Form001APIView(FormParameterAPIView):
    process_id = None
    form_id = form_constants.LOGIN

    def __init__(self):
        super().__init__()

    def post_post(self, request):
        super().post_post(request)
        username = self.parameters['username']
        password = self.parameters['password']

        # TODO: here is where I will authenticate my user
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            self.data['refresh'] = str(refresh)
            self.data['access'] = str(refresh.access_token)
            self.data['redirect'] = f'navigator/{page_constants.HOME}'
            self.data['user'] = get_user_profile(user, True)
            # self.data['user'] = UserSerializer(user).data
            # self.data['user']['is_logged_in'] = True
        else:
            message = 'Invalid username or password'
            self.set_message(message, http_status_id=status_constants.HTTP_UNAUTHORIZED)

            # token, created = Token.objects.get_or_create(user=user)

