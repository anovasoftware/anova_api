from core.services.job_service import JobService
from constants import type_constants, status_constants
from apps.res.models import Event, Room, EventRoom
from apps.static.models import Hotel


class EventRoomService(JobService):
    def _process(self):
        self.populate_event_room()

    def populate_event_room(self, hotel_id=None, event_id=None, room_id=None):
        self.success = True  # dummy

        hotels = Hotel.objects.filter(
            status_id=status_constants.ACTIVE
        )

        if hotel_id:
            hotels = hotels.filter(hotel_id=hotel_id)

        for hotel in hotels:
            events = Event.objects.filter(
                hotel_id=hotel.hotel_id,
                type_id=type_constants.RES_EVENT_CRUISE,
                status_id=status_constants.ACTIVE,
            ).order_by(
                'start_date'
            )
            rooms = Room.objects.filter(
                hotel_id=hotel.hotel_id,
                type_id__in=[
                    type_constants.RES_ROOM_CABIN,
                    type_constants.RES_ROOM_HOTEL_ROOM
                ],
                status_id=status_constants.ACTIVE
            ).order_by(
                'code'
            )

            if event_id:
                events = events.filter(event_id=event_id)

            if room_id:
                rooms = rooms.filter(room_id=room_id)

            for event in events:
                for room in rooms:
                    event_room, created = EventRoom.objects.get_or_create(
                        event_id=event.event_id,
                        room_id=room.room_id,
                        defaults={
                            'type_id': type_constants.NOT_APPLICABLE,
                            'status_id': status_constants.ACTIVE,
                            'inventory_status_id': status_constants.EVENT_ROOM_AVAILABLE
                        }
                    )

