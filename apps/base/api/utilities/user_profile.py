from rest_framework.permissions import IsAuthenticated
from core.api_views.core_api import CoreAPIView
from apps.base.utilities.user_utilities import get_user_profile


class UserProfileAPIView(CoreAPIView):
    permission_classes = [IsAuthenticated]
    process_id = None

    def _get(self, request):
        self.data['user'] = get_user_profile(request.user, True)
