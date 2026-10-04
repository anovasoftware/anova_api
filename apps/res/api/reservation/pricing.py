from decimal import Decimal

from apps.res.api_views.res_api_views import AuthorizedResAPIView
from apps.res.models import EventCategoryPrice
from constants import process_constants, type_constants, status_constants, currency_constants
from django.db.models import QuerySet


class ReservationPricingAPIView(AuthorizedResAPIView):
    process_id = process_constants.RESERVATION_PRICING
    http_method_names = ['post', 'options', 'head']
    PARAM_NAMES = AuthorizedResAPIView.PARAM_NAMES + ('eventId', 'currencyId', 'rateTypeId')
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_post=True,
            default=None,
            allowed=(
                type_constants.EVENT_CATEGORY_PRICE_STANDARD,
            ),
        ),
        'rateTypeId': dict(
            required_post=True,
            default=None,
            allowed=(
                type_constants.EVENT_CATEGORY_PRICE_RATE_FIT,
            ),
        ),
        'eventId': dict(
            required_post=True,
            default=None
        ),
        'currencyId': dict(
            required_post=True,
            default=None
        ),
    }

    def __init__(self):
        super().__init__()
        self.event_category_prices: QuerySet[EventCategoryPrice] = EventCategoryPrice.objects.none()
        self.request_data_required = True

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def load_models(self, request, *args, **kwargs):
        super().load_models(request)

    def _post(self, request, *args, **kwargs):
        type_id = self.type_id
        rate_type_id = self.rate_type_id
        currency_id = self.currency_id


        event_id = self.params.get('eventId')
        reservation_rooms0 = self.request_data[0].get('reservation_rooms', [])
        reservation_rooms = []

        # self.data['currency_id'] = currency_id
        self.data['reservation_rooms'] = reservation_rooms
        print(self.params)
        print(self.request_data)

        self.event_category_prices = EventCategoryPrice.objects.filter(
            currency_id=currency_id,
            event_id=event_id,
            type_id=type_id,
            status_id=status_constants.ACTIVE,
            rate_type_id=rate_type_id
        ).exclude(
            price=0.00
        )

        reservation_total = Decimal('0.00')
        room_number = 0
        for reservation_room in reservation_rooms0:
            room_number += 1
            guest_number = 0


            # reservation_room['room_number'] = str(room_number).zfill(2)
            category_id = reservation_room['category_id']
            adult_count = int(reservation_room['adult_count'])
            child_count = int(reservation_room['child_count'])
            infant_count = int(reservation_room['infant_count'])
            guest_count = adult_count + child_count + infant_count

            guests = []
            for i in range(1, adult_count + 1):
                guest_number += 1
                ecp = self.get_event_category_price(reservation_room, 'adult', guest_number)
                guest = {
                    'guest_number': str(guest_number).zfill(2),
                    'event_category_price': ecp
                }
                guests.append(guest)

            for i in range(1, child_count + 1):
                guest_number += 1
                ecp = self.get_event_category_price(reservation_room, 'child', guest_number)
                guest = {
                    'guest_number': str(guest_number).zfill(2),
                    'event_category_price': ecp
                }
                guests.append(guest)

            for i in range(1, infant_count + 1):
                guest_number += 1
                ecp = self.get_event_category_price(reservation_room, 'infant', guest_number)
                guest = {
                    'guest_number': str(guest_number).zfill(2),
                    'event_category_price': ecp
                }
                guests.append(guest)


            room = {
                'room_number': str(room_number).zfill(2),
                'category_id': category_id,
                'reservation_room_guests': guests,
            }
            reservation_rooms.append(room)

    def get_event_category_price(self, reservation_room, guest_type, guest_number):
        event_category_price = {}
        occupancy_type_id = None
        category_id = reservation_room['category_id']
        adult_count = int(reservation_room['adult_count'])
        child_count = int(reservation_room['child_count'])
        infant_count = int(reservation_room['infant_count'])

        if guest_type == 'adult':
            if adult_count == 1:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_SINGLE
            elif adult_count > 1 and guest_number in [1, 2]:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE
            elif adult_count == 3:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_THIRD_GUEST
            elif adult_count >= 4:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_FOURTH_GUEST
            else:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE

        if guest_type == 'child':
            occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_CHILD

        if guest_type == 'infant':
            occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_INFANT


        if occupancy_type_id is not None:
            event_category_prices = self.event_category_prices.filter(
                category_id=category_id,
                occupancy_type_id=occupancy_type_id,
            )

            cnt = event_category_prices.count()
            if cnt == 0:
                self.add_message('Pricing not configured', status_constants.HTTP_BAD_REQUEST)
            elif cnt > 2:
                self.add_message('unique pricing not established', status_constants.HTTP_BAD_REQUEST)

            if self.success:
                ecp = event_category_prices.first()

                event_category_price = {
                    'event_category_price_id': ecp.event_category_price_id,
                    'type_id': ecp.type_id,
                    'event_id': ecp.event_id,
                    'category_id': ecp.category_id,
                    'currency_id': ecp.currency_id,
                    'rate_type_id': ecp.rate_type_id,
                    'occupancy_type_id': ecp.occupancy_type_id,
                    'price': ecp.price
                }

        return event_category_price

