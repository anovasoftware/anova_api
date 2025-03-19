from django.core.exceptions import ObjectDoesNotExist

from core.api_views.table_api_views import AuthorizedTableAPIView
from apps.static.models import Client


class AuthorizedClientAPIView(AuthorizedTableAPIView):
    def __init__(self):
        super().__init__()
        self.client_id = None
        self.client = None

    def load_request(self, request):
        super().load_request(request)
        self.client_id = self.get_param('clientId', None, True)

        if self.success:
            try:
                client = Client.objects.get(pk=self.client_id)
            except ObjectDoesNotExist as e:
                self.add_message(f'invalid clientId: {self.client_id}', success=False)

    def get_query_filter(self):
        filters = super().get_query_filter()

        filters['client_id'] = self.client_id

        return filters  # This will be used in queryset.filter()
