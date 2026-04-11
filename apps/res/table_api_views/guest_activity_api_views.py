from apps.static.table_api_views.hotel_api_views import AuthorizedHotelAPIView
from apps.res.models import GuestActivity, Guest

from constants import type_constants, process_constants, status_constants


class AuthorizedGuestActivityAPIView(AuthorizedHotelAPIView):
    pass


class AuthorizedGuestActivityGangwayAPIView(AuthorizedGuestActivityAPIView):
    process_id = process_constants.RES_GUEST_ACTIVITY_GANGWAY

    PARAM_NAMES = AuthorizedHotelAPIView.PARAM_NAMES + ('rfidUid',)
    PARAM_OVERRIDES = {
        'typeId': dict(required_get=True, required_post=False, allowed=(type_constants.NOT_APPLICABLE,)),
        'hotelPublicKey': dict(required_get=False, required_post=True,),
        'rfidUid': dict(required_get=True, required_post=True,),

    }

    def __init__(self):
        super().__init__()
        self.app_name = 'res'
        self.model_name = 'GuestActivity'
        self.rfid_uid = None
        self.guest = None
        # self.accepted_type_ids = [
        #     type_constants.NOT_APPLICABLE,
        #     type_constants.RES_GUEST_GUEST,
        #     type_constants.RES_GUEST_CREW,
        #     type_constants.RES_GUEST_STAFF
        # ]

    def load_request(self, request):
        super().load_request(request)

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            try:
                self.guest = Guest.objects.get(rfid_uid=self.rfid_uid)
            except Guest.DoesNotExist:
                message = f'Guest not found for rfid_uid: {self.rfid_uid}'
                self.set_message(message, http_status_id=status_constants.HTTP_BAD_REQUEST)
    # def get_value_list(self):
    #     value_list = [
    #         'guest_id',
    #         'authorized_to_charge_flag',
    #         'type__type_id',
    #         'type__code',
    #         'type__description',
    #         'person__first_name',
    #         'person__last_name'
    #     ] + super().get_value_list()
    #
    #     return value_list
    #
    # def get_query_filter(self):
    #     filters = super().get_query_filter()
    #
    #     filters['type_id'] = self.type_id
    #
    #     return filters

