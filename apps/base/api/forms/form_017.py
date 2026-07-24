from apps.static.models import FormField
from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants, type_constants
from apps.base.models import UserRole, ClientCurrency
from core.utilities.date_utilities import end_of_time, today


class Form017APIView(AuthorizedFormAPIView):
    # PARAM_OVERRIDES = {
    #     'typeId': dict(
    #         required_get=True,
    #         required_post=True,
    #     ),
    # }

    process_id = process_constants.FORM_017
    form_id = form_constants.CLIENT_CURRENCY

    def __init__(self):
        super().__init__()
        self.client_currencies = None

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            self.client_currencies = ClientCurrency.objects.filter(
                client_id=self.client_id
            )

    def get_data_options_selected(self, field: FormField):
        if field.data_source_key == 'CURRENCIES':
            data_options_selected = list(
                self.client_currencies.filter(
                    status_id=status_constants.ACTIVE,
                ).values_list(
                    'currency_id', flat=True
                )
            )
        else:
            data_options_selected = super().get_data_options_selected(field)

        return data_options_selected

    def _post(self, request):
        super()._post(request)

        record = self.record
        selected_currencies = record.get('selected_currencies', [])

        client_currencies_to_inactivate = self.client_currencies.exclude(
            currency_id__in=selected_currencies
        )
        client_currencies_to_inactivate = client_currencies_to_inactivate.filter(
            static_flag='N',
        )
        client_currencies_to_inactivate.update(
            status_id=status_constants.INACTIVE,
            end_date=today(),
            effective_status_id=status_constants.EFFECTIVE_STATUS_EXPIRED
        )
        for currency_id in selected_currencies:
            client_currency, created = ClientCurrency.objects.update_or_create(
                client_id=self.client_id,
                currency_id=currency_id,
                defaults={
                    'status_id': status_constants.ACTIVE,
                    'end_date': end_of_time(),
                    'effective_status_id': status_constants.EFFECTIVE_STATUS_CURRENT,
                }
            )
