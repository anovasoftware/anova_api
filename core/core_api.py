import os
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import status
from rest_framework.request import Request
from constants import constants
from anova_api.configuration.database import get_database_property
from apps.static.models import Status


class CoreAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.success = True
        self.debug_flag = 'N'
        self.params = {}
        self.message = 'call successful'
        self.messages = []
        self.data = {}
        self.request_id = ''

    def load_request(self, request):
        self.request_id = getattr(request, "request_id", "unknown")
        self.debug_flag = self.get_param('debugFlag', 'N', False)
        # self.user_id = request.user.user_id
        # self.access_user_id = request.user.access_user_id

    def get_param(self, key, default_value, required):
        ret_value = default_value
        params: Request = self.request.query_params

        if key in params:
            ret_value = params[key]

        if required and not ret_value:
            self.message = 'missing parameter(s)'
            self.add_message(f'missing parameter: {key}', success=False)

        if key != 'debugFlag':
            self.params[key] = ret_value
        return ret_value

    def add_message(self, message, success=True):
        self.messages.append(message)
        self.success = self.success and success

    def get(self, request):
        try:
            self.load_request(request)
            # if self.status == 200:
            if self.success:
                self.pre_get(request)
                if self.success:
                    if self.success:
                        self._get(request)
                        if self.success:
                            self.post_get(request)
        except Exception as e:
            self.add_message(f'get() error:  {str(e)}', success=False)

        return self.get_response()

    def pre_get(self, request):
        pass

    def _get(self, request):
        self.add_message('get() not defined', success=False)

    def post_get(self, request):
        pass

    def get_response(self):
        status = 'success' if self.success else 'error'
        response = {
            'meta': {
                'version': constants.VERSION,
                'database-key': os.getenv('DATABASE_KEY'),
                'database-id':  os.getenv('DATABASE_ID'),
                'request-id': self.request_id,
                'supplied-parameters': self.params,
            },
            'status': status,
            'message': self.message,
            'messages': self.messages,
            'data': self.data,
        }
            #
            # 'database-host': get_database_property('HOST'),
            # 'database-name': get_database_property('NAME'),
            #
            #

        return Response(response)

    # def success_response(self, data=None, message="Success", status_code=status.HTTP_200_OK):
    #     return Response({
    #         "success": self.success,
    #         "message": message,
    #         "data": data if data is not None else {},
    #     }, status=status_code)
    #
    # @staticmethod
    # def error_response(errors=None, message="An error occurred", status_code=status.HTTP_400_BAD_REQUEST):
    #     return Response({
    #         "success": False,
    #         "message": message,
    #         "errors": errors if errors is not None else [],
    #     }, status=status_code)


class TestAPI(CoreAPIView):
    def __init__(self):
        super().__init__()
        self.param1 = False

    def load_request(self, request):
        super().load_request(request)
        self.param1 = self.get_param('param1', None, True)

    def _get(self, request):
        self.add_message('_get() successful')
        self.data['status'] = 'some status'
        # try:
        #     status_obj = Status.objects.get(pk='00s1')
        #     self.data['status'] = status_obj.description
        # except Exception as e:
        #     self.add_message(f'error {str(e)}', success=False)


    # def post(self, request):
    #     if not request.data.get("name"):
    #         return self.error_response(message="Name is required", errors=["Missing 'name' field"])
    #     return self.success_response(data={"name": request.data["name"]}, message="Data received")
class GuestRoomAPI(CoreAPIView):
    def __init__(self):
        super().__init__()
        self.hotel_id = ''
        self.room_id = False

    def load_request(self, request):
        super().load_request(request)
        self.hotel_id = self.get_param('hotel_id', '', True)
        self.room_id = self.get_param('room_id', '', True)

    def _get(self, request):
        status = Status.objects.get(pk='001')
        self.message = 'under construction'
        self.data['hotel_id'] = self.hotel_id
        self.data['hotel_description'] = 'Magellan Explorer'
        self.data['status'] = status.description


# JSON response
# {
#    "Status":1,
#    "HotelId":"HOTEL1",
#    "HotelName":"Hotel Inn",
#    "ReservationId":"0005897961",
#    "ReservationStatus":6,
#    "ChannelId":"OTA",
#    "BookingPlatform":"Booking.com",
#    "CreatedDate":"2022-11-23",
#    "CreatedTime":"11:33:44",
#    "CheckInDate":"2022-12-05",
#    "CheckOutDate":"0000-00-00",
#    "Pax":1,
#    "PMSIRooms":[
#       {
#          "RoomNumber":"301",
#          "RoomType":"STD",
#          "PMSIGuests":[
#             {
#                "GuestName":"John Doe",
#                "GuestId":"0021141211",
#                "FirstName":"John",
#                "LastName":"Doe",
#                "Email":"John@Doe.com",
#                "Gender":1,
#                "Birthday":"2000-11-20",
#                "Mobile":"1234567890",
#                "Nationality":"Bahamas",
#                "DocumentNumber":"P0001241512",
#                "DocumentType":1
#             }
#          ]
#       }
#    ]
# }
