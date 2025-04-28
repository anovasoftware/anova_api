from rest_framework.permissions import BasePermission


class ThirdPartyAccessPermission(BasePermission):
    ALLOWED_ENDPOINTS = {
        '/api/allowed-endpoint-1/': ['GET'],
        '/api/allowed-endpoint-2/': ['POST'],
        '/api/allowed-endpoint-3/': ['GET', 'POST'],
    }

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        if not getattr(user, 'is_third_party', False):
            return False

        path = request.path_info
        method = request.method

        # Check if path is in allowed endpoints
        allowed_methods = self.ALLOWED_ENDPOINTS.get(path)
        if not allowed_methods:
            return False

        # Check if method is allowed for the path
        return method in allowed_methods
