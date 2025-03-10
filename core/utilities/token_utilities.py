from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import secrets


def generate_user_token(username: str):
    User = get_user_model()  # This ensures the correct User model is used
    try:
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        return token.key
    except User.DoesNotExist:
        return "User does not exist"


# in a python window:
# from core.utilities.token_utilities import generate_user_token
# generate_user_token('jburke@anovasoftware.com')
def generate_secure_token(length=40):
    return secrets.token_hex(length // 2)  # token_hex generates hex string, so divide length by 2


# # Example usage
# token = generate_secure_token()
# print(token)
