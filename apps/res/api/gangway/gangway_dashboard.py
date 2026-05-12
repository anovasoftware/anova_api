from django.db.models import QuerySet

from apps.res.api_views.res_api_views import AuthorizedResAPIView
from apps.res.models import Guest, GuestRoom
from apps.res.utilities.gangway_utilities import GangwayUtility
from apps.static.models import Type, Status
from constants import process_constants, type_constants


class GangwayDashboardAPIView(AuthorizedResAPIView):
    process_id = process_constants.GANGWAY_DASHBOARD
    http_method_names = ['get', 'options', 'head']
    # PARAM_NAMES = AuthorizedResAPIView.PARAM_NAMES
    # PARAM_OVERRIDES = {
    #     **getattr(AuthorizedAPIView, 'PARAM_OVERRIDES', {}),
    #     'hotelId': dict(
    #         required_get=True,
    #     ),
    #
    # }

    DOC_CONTEXT = {}

    def __init__(self):
        super().__init__()
        self.guests: QuerySet[Guest] = Guest.objects.none()
        self.guest_rooms: QuerySet[GuestRoom] = GuestRoom.objects.none()

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs)

    def load_models(self, request, *args, **kwargs):
        super().load_models(request)

        # if self.success:
        #     self.guest_rooms = GuestRoom.objects.filter(
        #         guest__reservation__hotel_id=self.hotel_id,
        #         arrival_date__gte=self.hotel_extension
        #         departure_date__gt=self.today,
        #     )


    def _get(self, request, *args, **kwargs):
        gangway_utility = GangwayUtility(self.hotel_extension.current_event)

        parent_type_ids = Type.objects.filter(
            grouping='res_guest'
        ).values_list(
            'parent_type_id', flat=True
        ).distinct()

        guest_types = Type.objects.filter(
            type_id__in=parent_type_ids,
        ).values(
            'type_id',
            'description',
        ).order_by(
            'order_by'
        )
        guest_statuses = Status.objects.filter(
            grouping='res_guest'
        ).values(
            'status_id',
            'description',
        ).order_by(
            'order_by'
        )

        self.data['lookups'] = {}
        self.data['lookups']['guest_types'] = list(guest_types)
        self.data['lookups']['guest_statuses'] = list(guest_statuses)
        self.data['counters'] = gangway_utility.get_guest_counts()



