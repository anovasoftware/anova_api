from apps.base.serializers.user import UserSerializer

def get_user_profile(user, is_logged_in=False):
    user = UserSerializer(user).data
    user['is_logged_in'] = is_logged_in

    return user