from apps.static.table_api_views.form_api_views import FormParameterAPIView
from constants import form_constants, status_constants, type_constants, person_constants
from apps.base.models import User, UserVerification
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.base.serializers.user import UserSerializer

# create an account
class Form002APIView(FormParameterAPIView):
    form_id = form_constants.CREATE_ACCOUNT

    def __init__(self):
        super().__init__()

    def get_field_value(self, field):
        value = ''
        if False:
            pass
        # elif field.get('name') == 'string01':
        #     value = 'jwburke@gmail.com'
        # elif field.get('name') == 'string02':
        #     value = 'Mr.'
        # elif field.get('name') == 'string03':
        #     value = 'John'
        # elif field.get('name') == 'string04':
        #     value = 'W.'
        # elif field.get('name') == 'string05':
        #     value = 'Burke'
        else:
            value = super().get_field_value(field)
        return value

    def validate_post(self, request):
        super().validate_post(request)

        username = self.parameters.get('username')
        password1 =  self.parameters.get('password1')
        password2 = self.parameters.get('password2')

        user = User.objects.filter(username=username).first()

        # if User.objects.filter(username=username).exists():
        if user:
            if user.status_id == status_constants.USER_PENDING:
                message = f'Account already exists. A verification email will be sent.'
                self.add_message(message, status_constants.HTTP_BAD_REQUEST)
                generate_user_verification(user)
            else:
                message = f'Username (email) {self.parameters.get("username")} already exists.'
                self.add_message(message, status_constants.HTTP_BAD_REQUEST)

        if password1 != password2:
            message = 'Passwords do not match.'
            self.add_message(message, status_constants.HTTP_BAD_REQUEST)

    def post_post(self, request):
        super().post_post(request)
        # person = Person.objects.create(
        #     type_id=type_constants.PERSON_REGULAR,
        #     first_name=self.parameters.get('first_name'),
        #     last_name=self.parameters.get('last_name'),
        #     email=self.parameters.get('username')
        # )
        user = User.objects.create_user(
            type_id=type_constants.USER_REAL,
            username=self.parameters.get('username'),
            password=self.parameters.get('password1'),
            person_id=person_constants.TO_BE_ANNOUNCED,
            status_id=status_constants.USER_PENDING,
            verification_status_id=status_constants.USER_VERIFICATION_REQUESTED,
            email=self.parameters.get('username')
        )
        user.access_user_id = user.user_id
        # user.description = person.__str__()
        user.save()
        generate_user_verification(user)


def generate_user_verification(user):
    user_id = user.user_id
    UserVerification.objects.filter(
        user_id=user_id,
        status__group1='0'
    ).update(
        status_id=status_constants.USER_VERIFICATION_CANCELLED
    )
    user_verification = UserVerification.objects.create(
        user_id=user.user_id,
        type_id=type_constants.BASE_USER_VERIFICATION_EMAIL,
        status_id=status_constants.USER_VERIFICATION_REQUESTED
    )