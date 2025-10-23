from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import secrets
from django.core.management.base import BaseCommand
import os
from core.utilities.logging_utilities import log_message


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
# generate_user_token('anova')
def generate_secure_token(length=40):
    return secrets.token_hex(length // 2)  # token_hex generates hex string, so divide length by 2
    # # Example usage
    # token = generate_secure_token()
    # print(token)


def initialize_tokens_from_env():
    User = get_user_model()
    updated = 0

    for key, value in os.environ.items():
        if key.startswith('TOKEN_'):
            user_id = key[6:]
            try:
                user = User.objects.get(pk=user_id)

                Token.objects.filter(user=user).delete()
                Token.objects.create(user=user, key=value)

                # token, created = Token.objects.update_or_create(
                #     user=user,
                #     defaults={
                #         'key': value
                #     }
                # )
                log_message(f'✓ Token set for user {user_id}')
                updated += 1
            except User.DoesNotExist:
                log_message(f"✗ User with ID {user_id} not found", message_type='red')
    log_message(f"✓ Token initialization complete: {updated} tokens updated.", 'green')
    log_message(f'NOTE: token initialization will not be applied in aws.', 'red')
