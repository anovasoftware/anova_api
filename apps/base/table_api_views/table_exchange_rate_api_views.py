from typing import Optional

from apps.static.models import Currency
from core.api_views.table_api_views import PublicTableAPIView
from django.core.cache import cache

from constants import type_constants, process_constants, job_constants
from apps.base.models import JobExtension


class ExchangeRateAPIView(PublicTableAPIView):
    process_id = process_constants.BASE_EXCHANGE_RATE

    PARAM_SPECS = PublicTableAPIView.PARAM_SPECS + ('typeId',)
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=False,
            allowed=(
                type_constants.EXCHANGE_RATE_LATEST,
            )
        )
    }

    @classmethod
    def get_cache_key_pattern(cls):
        return f'PROCESS-{cls.process_id}'

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'ExchangeRate'
        self.order_by = ['currency__code']
        # self.job_extension: Optional[JobExtension] = None

    # def load_models(self, request):
    #     super().load_models(request)
    #
    #     self.job_extension = JobExtension.objects.get(job_id=job_constants.EXCHANGE_RATE_SERVICE)

    def get_value_list(self):
        value_list = [
            'currency__currency_id',
            'currency__code',
            'rate'
        ] + super().get_value_list()
        return value_list

    def get_query_filter(self):
        currencies = Currency.objects.exclude(
            currency_id=self.home_currency['currency_id']
        ).values_list(
            'currency_id', flat=True
        )

        filters = super().get_query_filter()
        filters['currency_id__in'] = currencies

        return filters  # This will be used in queryset.filter()

    def _get(self, request):
        # cache_key = f'exchange_rate_api:type_id:{self.type_id}'
        cache_key = f'{self.get_cache_key_pattern()}.{self.type_id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            self.data = cached_data
            self.data['cached'] = True
            return

        super()._get(request)

        self.data['cached'] = False
        self.data['home_currency'] = self.home_currency

        job = JobExtension.objects.get(job_id=job_constants.EXCHANGE_RATE_SERVICE)
        job = {
            'job_id': job.job_id,
            'description': job.job.description,
            'job_extension_id': job.job_extension_id,
            'last_run_time': job.last_run_time,
        }

        self.data['job'] = job
        self.data['rates'] = self.records

        cache.set(cache_key, self.data, timeout=3600)
