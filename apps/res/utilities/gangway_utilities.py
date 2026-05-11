from django.db.models import Count
from apps.res.models import GuestRoom, Event
from typing import Optional
from django.utils import timezone

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

        for row in counts:
            row['type_id'] = row.pop('guest__type_id')
            row['status_id'] = row.pop('guest__status_id')

        return counts
