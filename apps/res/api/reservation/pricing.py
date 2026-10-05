from decimal import Decimal

from apps.base.models import Category
from apps.res.api_views.res_api_views import AuthorizedResAPIView
from apps.res.models import EventCategoryPrice
from constants import process_constants, type_constants, status_constants, currency_constants, category_constants
from django.db.models import QuerySet
from django.db.models import F


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

    def load_lookups(self):
        super().load_lookups()

        self.add_lookup(
            lookup_name='category',
            param_name='categoryId',
            label='Category',
            options=self.get_category_lookup(type_id=type_constants.BASE_CATEGORY_ROOM_CABIN),
            selected_id=category_constants.BASE_CATEGORY_NOT_APPLICABLE
        )

        self.add_lookup(
            lookup_name='occupancy_type',
            param_name='typeId',
            label='Type',
            options=self.get_type_lookup(grouping='event_category_price.occupancy'),
            selected_id=category_constants.BASE_CATEGORY_NOT_APPLICABLE
        )

    def get_category_lookup(self, type_id=None):
        categories = Category.objects.filter(
            hotel_id=self.hotel_id,
            type_id=type_id,
            status_id=status_constants.ACTIVE
        ).values(
            'description',
            id=F('category_id'),
        )
        return categories



    def _post(self, request, *args, **kwargs):
        print(self.request_data)
        type_id = self.type_id
        rate_type_id = self.rate_type_id
        currency_id = self.currency_id
        event_id = self.params.get('eventId')

        reservation_rooms0 = self.request_data[0].get('reservation_rooms', [])
        reservation_rooms = []
        self.data['reservation_rooms'] = reservation_rooms

        self.event_category_prices = EventCategoryPrice.objects.filter(
            currency_id=currency_id,
            event_id=event_id,
            type_id=type_id,
            status_id=status_constants.ACTIVE,
            rate_type_id=rate_type_id
        ).exclude(
            price=0.00
        )

        for reservation_room in reservation_rooms0:
            category_id = reservation_room['category_id']

            reservation_room_guests = reservation_room.get('reservation_room_guests', [])
            guests = []

            for reservation_room_guest in reservation_room_guests:
                guest_number = reservation_room_guest['guest_number']
                guest_type_id = reservation_room_guest['occupancy_type_id']

                ecp = self.get_event_category_price(
                    reservation_room,
                    reservation_room_guests,
                    guest_type_id,
                    guest_number
                )

                guests.append({
                    'guest_number': guest_number,
                    'event_category_price': ecp
                })

            room = {
                'room_number': reservation_room['order_by'],
                'category_id': category_id,
                'reservation_room_guests': guests,
            }

            reservation_rooms.append(room)

    def get_event_category_price(
            self,
            reservation_room,
            reservation_room_guests,
            guest_type_id,
            guest_number
    ):
        event_category_price = {}
        occupancy_type_id = None

        category_id = reservation_room['category_id']

        if guest_type_id == type_constants.RESERVATION_ROOM_GUEST_ADULT:
            adult_guests = [
                guest for guest in reservation_room_guests if guest['occupancy_type_id']  == guest_type_id
            ]
            adult_count = len(adult_guests)

            adult_guest_numbers = [ guest['guest_number'] for guest in adult_guests]
            adult_position = adult_guest_numbers.index(guest_number) + 1

            if adult_count == 1:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_SINGLE

            elif adult_position <= 2:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_DOUBLE

            elif adult_position == 3:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_THIRD_GUEST
            else:
                occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_FOURTH_GUEST
        elif guest_type_id == type_constants.RESERVATION_ROOM_GUEST_CHILD:
            occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_CHILD
        elif guest_type_id == type_constants.RESERVATION_ROOM_GUEST_INFANT:
            occupancy_type_id = type_constants.EVENT_CATEGORY_PRICE_OCCUPANCY_INFANT

        # ---------------------------------------------------------
        # Find EventCategoryPrice
        # ---------------------------------------------------------
        if occupancy_type_id is not None:
            event_category_prices = self.event_category_prices.filter(
                category_id=category_id,
                occupancy_type_id=occupancy_type_id,
            )

            cnt = event_category_prices.count()

            if cnt == 0:
                self.add_message('Pricing not configured', status_constants.HTTP_BAD_REQUEST)
            elif cnt > 1:
                self.add_message('Unique pricing not established', status_constants.HTTP_BAD_REQUEST)
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