import pandas as pd
from django.db.models import Count
from apps.res.models import GuestRoom, Event
from typing import Optional
from django.utils import timezone
from collections import defaultdict

today = timezone.localdate()


class GangwayUtility:
    def __init__(self, event):
        super().__init__()
        self.event: Optional[Event] = event

        self.as_of_date = today
        if today < event.event_start_date:
            self.as_of_date = event.event_start_date
        elif today > event.event_end_date:
            self.as_of_date = event.event_end_date

    def get_guest_counts(self):
        event = self.event

        guest_rooms = GuestRoom.objects.filter(
            guest__reservation__hotel_id=event.hotel_id
        )

        if self.as_of_date == event.event_start_date:
            # embarkation/changeover afternoon for this cruise
            guest_rooms = guest_rooms.filter(
                arrival_date__lte=self.as_of_date,
                departure_date__gt=self.as_of_date,
            )

        elif self.as_of_date == event.event_end_date:
            # disembarkation/changeover morning for this cruise
            guest_rooms = guest_rooms.filter(
                arrival_date__lt=self.as_of_date,
                departure_date__gte=self.as_of_date,
            )

        else:
            # normal cruise day
            guest_rooms = guest_rooms.filter(
                arrival_date__lte=self.as_of_date,
                departure_date__gt=self.as_of_date,
            )

        # guest_rooms_df = pd.DataFrame(
        #     guest_rooms.values(
        #         'guest_id',
        #         'guest__type_id',
        #         'guest__status_id',
        #         'arrival_date',
        #         'departure_date',
        #     )
        # )
        # print(guest_rooms_df)
        # debug_df = guest_rooms_df.copy()
        # debug_df = debug_df.reset_index(drop=True)
        # debug_df = debug_df.astype({
        #     'guest_id': 'string',
        #     'guest__type_id': 'string',
        #     'guest__status_id': 'string',
        #     'arrival_date': 'string',
        #     'departure_date': 'string',
        # })
        counts = guest_rooms.values(
            'guest__type_id',
            'guest__status_id'
        ).annotate(
            count=Count('guest_id', distinct=True)
        ).order_by(
            'guest__type_id',
            'guest__status_id',
        )

        counts = list(counts)

        # for row in counts:
        #     row['type_id'] = row.pop('guest__type_id')
        #     row['status_id'] = row.pop('guest__status_id')

        results = []
        type_totals = defaultdict(int)
        status_totals = defaultdict(int)
        grand_total = 0

        for row in counts:
            type_id = row['guest__type_id']
            status_id = row['guest__status_id']
            count = int(row['count'] or 0)

            results.append({
                'type_id': type_id,
                'status_id': status_id,
                'count': count,
            })

            type_totals[type_id] += count
            status_totals[status_id] += count
            grand_total += count

        for type_id, count in type_totals.items():
            results.append({
                'type_id': type_id,
                'status_id': 'TOT',
                'count': count,
            })

        for status_id, count in status_totals.items():
            results.append({
                'type_id': 'TOT',
                'status_id': status_id,
                'count': count,
            })

        results.append({
            'type_id': 'TOT',
            'status_id': 'TOT',
            'count': grand_total,
        })

        return results