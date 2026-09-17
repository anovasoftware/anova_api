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

        EventCategoryPrice.objects.filter(
            type_id=type_constants.NOT_APPLICABLE
        ).update(
            type_id=type_constants.EVENT_CATEGORY_PRICE_STANDARD
        )

        hotels = Hotel.objects.filter(
            status_id=status_constants.ACTIVE,
            type_id=type_constants.HOTEL_CRUISE_SHIP
        )
        types = Type.objects.filter(
            grouping='event_category_price'
        ).order_by(
            'order_by'
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
                        for type_ in types:
                            for rate_type in rate_types:
                                for occupancy_type in occupancy_types:
                                    event_category_price, created = EventCategoryPrice.objects.get_or_create(
                                        type_id=type_.type_id,
                                        event_id=event.event_id,
                                        category_id=category.category_id,
                                        currency_id=currency.currency_id,
                                        rate_type_id=rate_type.type_id,
                                        occupancy_type_id=occupancy_type.type_id,
                                    )


