from apps.base.models import ClientCurrency
from apps.static.models import Currency
from apps.res.models import ClientExtension
from core.services.job_service import JobService
from constants import type_constants, status_constants, currency_constants


def get_client_extension(client_id: str):
    client_extension, _ = ClientExtension.objects.get_or_create(
        client_id=client_id
    )
    return client_extension


class ClientService(JobService):
    def _process(self):
        self.populate_client_currency()

    def populate_client_currency(self):
        self.success = True  # dummy

        client_extensions = ClientExtension.objects.filter(
            client__type_id__in=[
                type_constants.CLIENT_CRUISE_LINE,
                type_constants.CLIENT_HOTEL_OPERATOR
            ]
        )
        currencies = Currency.objects.filter(
            type_id__in=[
                type_constants.CURRENCY_REAL
            ]
        )
        for client_extension in client_extensions:
            home_currency_id = client_extension.currency_id

            if home_currency_id != currency_constants.NOT_APPLICABLE:
                for currency in currencies:
                    status_id = status_constants.ACTIVE if currency.currency_id == home_currency_id else status_constants.INACTIVE
                    client_currency, created = ClientCurrency.objects.get_or_create(
                        client_id=client_extension.client_id,
                        currency_id=currency.currency_id,
                        defaults={
                            'status_id': status_id
                        }
                    )
                    self.records_created += 1 if created else 0
