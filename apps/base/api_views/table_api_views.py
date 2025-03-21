from django.core.exceptions import ObjectDoesNotExist
from core.api_views.table_api_views import AuthorizedTableAPIView
from apps.static.models import Client
from constants import client_constants


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
        client_ids = [self.client_id, client_constants.NOT_APPLICABLE]

        filters['client_id__in'] = client_ids

        return filters  # This will be used in queryset.filter()

    def get_value_list(self):
        value_list = [
            'client__client_id',
            'client__description',
         ] + super().get_value_list()

        return value_list
