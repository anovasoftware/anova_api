from decimal import Decimal

from apps.res.api_views.res_api_views import AuthorizedResAPIView
from apps.res.models import EventCategoryPrice
from constants import process_constants, type_constants, status_constants, currency_constants
from typing import Optional


class ReservationPricingAPIView(AuthorizedResAPIView):
    process_id = process_constants.RESERVATION_PRICING
    http_method_names = ['post', 'options', 'head']
    PARAM_NAMES = AuthorizedResAPIView.PARAM_NAMES + ('eventId',)
    PARAM_OVERRIDES = {
        'eventId': dict(
            required_post=True,
            default=None
        ),
    }

    def __init__(self):
        super().__init__()
        self.event_category_prices: Optional[EventCategoryPrice] = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def load_models(self, request, *args, **kwargs):
        super().load_models(request)

    def _post(self, request, *args, **kwargs):
        # TODO: these should come from frontend
        event_category_price_type_id = type_constants.EVENT_CATEGORY_PRICE_STANDARD
        event_category_price_rate_type_id = type_constants.EVENT_CATEGORY_PRICE_RATE_FIT
        currency_id = currency_constants.USD

        event_id = self.params.get('eventId')
        reservation_rooms0 = self.request_data[0].get('reservation_rooms', [])
        reservation_rooms = []

        self.data['currency_id'] = currency_id
        self.data['reservation_rooms'] = reservation_rooms
        print(self.params)
        print(self.request_data)

        self.event_category_prices = EventCategoryPrice.objects.filter(
            currency_id=currency_id,
            event_id=event_id,
            type_id=event_category_price_type_id,
            status_id=status_constants.ACTIVE,
            rate_type_id=event_category_price_rate_type_id
        ).exclude(
            price=0.00
        )

        reservation_total = Decimal('0.00')
        room_number = 0
        for reservation_room in reservation_rooms0:
            room_number += 1

            # reservation_room['room_number'] = str(room_number).zfill(2)
            category_id = reservation_room['category_id']
            adult_count = int(reservation_room['adult_count'])
            child_count = int(reservation_room['child_count'])
            infant_count = int(reservation_room['infant_count'])
            guest_count = adult_count + child_count + infant_count

            guests = []
            for guest_number in range(1, adult_count + 1):
                guest = {
                    'guest_number': str(guest_number).zfill(2),
                    'event_catgory_price': self.get_event_category_price('adult', guest_number, adult_count)
                }
                guests.append(guest)

            room = {
                'room_number': str(room_number).zfill(2),
                'category_id': category_id,
                'reservation_room_guests': guests,
            }
            reservation_rooms.append(room)

            # reservation_room_guests = []
            # room_total = Decimal('0.00')
            #
            # for guest_number in range(1, adult_count + 1):
            #     if adult_count == 1:
            #         event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_SINGLE
            #     elif adult_count > 1 and guest_number in [1, 2]:
            #         event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE
            #     elif guest_number == 3:
            #         event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_THIRD_GUEST
            #     elif guest_number >= 4:
            #         event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_FOURTH_GUEST
            #     else:
            #         event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE
            #
            #     guest = self.build_guest_price(
            #         event_category_prices,
            #         category_id,
            #         guest_number,
            #         event_category_price_occupancy_type_id,
            #         event_category_price_type_id,
            #         event_category_price_rate_type_id
            #     )
            #
            #     reservation_room_guests.append(guest)
            #     room_total += guest['price']
            #
            # for guest_number in range(1, child_count + 1):
            #     guest = self.build_guest_price(
            #         event_category_prices,
            #         category_id,
            #         guest_number,
            #         type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_CHILD,
            #         event_category_price_type_id,
            #         event_category_price_rate_type_id
            #     )
            #     reservation_room_guests.append(guest)
            #     room_total += guest['price']
            #
            # for guest_number in range(1, infant_count + 1):
            #     guest = self.build_guest_price(
            #         event_category_prices,
            #         category_id,
            #         guest_number,
            #         type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_INFANT,
            #         event_category_price_type_id,
            #         event_category_price_rate_type_id
            #     )
            #     reservation_room_guests.append(guest)
            #     room_total += guest['price']
            #
            # reservation_room['reservation_room_guests'] = reservation_room_guests
            # reservation_room['room_total'] = room_total
            # reservation_total += room_total
            #
            # self.data['total_price'] = reservation_total

    def get_event_category_price(self, guest_type, guest_number, guest_count):
        ecp = self.event_category_prices
        event_category_price = {}

        if guest_type == 'adult':
            if guest_count == 1:
                event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_SINGLE
            elif guest_count > 1 and guest_number in [1, 2]:
                event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE
            elif guest_count == 3:
                event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_THIRD_GUEST
            elif guest_number >= 4:
                event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_FOURTH_GUEST
            else:
                event_category_price_occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE

            event_category_price['occupancy_type_id'] = event_category_price_occupancy_type_id
            # guest = self.build_guest_price(
            #     event_category_prices,
            #     category_id,
            #     guest_number,
            #     event_category_price_occupancy_type_id,
            #     event_category_price_type_id,
            #     event_category_price_rate_type_id
            # )
            #
            # reservation_room_guests.append(guest)
            # room_total += guest['price']

        return event_category_price

    @staticmethod
    def build_guest_price(
            event_category_prices,
            category_id,
            guest_number,
            occupancy_type_id,
            price_type_id,
            rate_type_id
    ):
        prices = event_category_prices.filter(
            category_id=category_id,
            occupancy_type_id=occupancy_type_id
        )

        if prices.count() == 1:
            price = prices.first().price
        else:
            price = Decimal('0.00')

        guest = {
            'guest_number': guest_number,
            'event_category': {
                'price_type_id': price_type_id,
                'occupancy_type_id': occupancy_type_id,
                'rate_type_id': rate_type_id,
            },
            'price': price
        }

        return guest
