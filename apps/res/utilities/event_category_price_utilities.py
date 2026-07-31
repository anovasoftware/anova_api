from apps.base.models import Category, ClientCurrency
from core.services.job_service import JobService
from constants import type_constants, status_constants
from apps.res.models import Event, EventCategoryPrice
from apps.static.models import Hotel, Type


class EventCategoryPriceService(JobService):
    def _process(self):
        self.populate_event_category_price()

    def populate_event_category_price(self, hotel_id=None, event_id=None, room_id=None):
        self.success = True  # dummy

        hotels = Hotel.objects.filter(
            status_id=status_constants.ACTIVE,
            type_id=type_constants.HOTEL_CRUISE_SHIP
        )
        rate_types = Type.objects.filter(
            grouping='event_category_price.rate'
        ).order_by(
            'order_by'
        )
        occupancy_types = Type.objects.filter(
            grouping='event_category_price.occupancy'
        ).order_by(
            'order_by'
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
            categories = Category.objects.filter(
                hotel_id=hotel.hotel_id,
                status_id=status_constants.ACTIVE,
                type_id=type_constants.BASE_CATEGORY_ROOM_CABIN
            ).order_by(
                'code'
            )
            currencies = ClientCurrency.objects.filter(
                client_id=hotel.client_id,
                status_id=status_constants.ACTIVE
            )

            for event in events:
                for category in categories:
                    for currency in currencies:
                        for rate_type in rate_types:
                            for occupancy_type in occupancy_types:
                                event_category_price, created = EventCategoryPrice.objects.get_or_create(
                                    event_id=event.event_id,
                                    category_id=category.category_id,
                                    currency_id=currency.currency_id,
                                    rate_type_id=rate_type.type_id,
                                    occupancy_type_id=occupancy_type.type_id,
                                )


        #     rooms = Room.objects.filter(
        #         hotel_id=hotel.hotel_id,
        #         type_id__in=[
        #             type_constants.RES_ROOM_CABIN,
        #             type_constants.RES_ROOM_HOTEL_ROOM
        #         ],
        #         status_id=status_constants.ACTIVE
        #     ).order_by(
        #         'code'
        #     )
        #
        #     if event_id:
        #         events = events.filter(event_id=event_id)
        #
        #     if room_id:
        #         rooms = rooms.filter(room_id=room_id)
        #
        #     for event in events:
        #         for room in rooms:
        #             event_room, created = EventRoom.objects.get_or_create(
        #                 event_id=event.event_id,
        #                 room_id=room.room_id,
        #                 defaults={
        #                     'type_id': type_constants.NOT_APPLICABLE,
        #                     'status_id': status_constants.ACTIVE,
        #                     'inventory_status_id': status_constants.EVENT_ROOM_AVAILABLE
        #                 }
        #             )
        #
