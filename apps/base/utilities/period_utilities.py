from django.utils import timezone
from datetime import datetime, time, timedelta

from core.services.job_service import JobService
from apps.base.models import Period
from constants import type_constants


class PeriodService(JobService):
    def __init__(self, job):
        super().__init__(job)

    def _process(self):
        self.update_period_table()

    def update_period_table(self):
        self.create_days(30)

    def create_days(self, days):
        start_day = timezone.localdate()
        end_day = start_day + timedelta(days=days)

        existing_codes = set(
            Period.objects.filter(
                type_id=type_constants.BASE_PERIOD_DAILY,
                start_date__gte=start_day,
            ).values_list('code', flat=True)
        )

        day = start_day
        while day <= end_day:
            yyyymmdd = day.strftime('%Y%m%d')
            if yyyymmdd not in existing_codes:
                start_date = timezone.make_aware(datetime.combine(day, time.min))
                end_date = timezone.make_aware(datetime.combine(day, time.max))
                defaults = {
                    'start_date': start_date,
                    'end_date': end_date
                }
                period, created = Period.objects.update_or_create(
                    type_id=type_constants.BASE_PERIOD_DAILY,
                    code=yyyymmdd,
                    defaults=defaults
                )
                if created:
                    self.records_created += 1
                else:
                    self.records_updated += 1

            day += timedelta(days=1)
