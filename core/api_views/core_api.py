import os
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from constants import constants
from apps.static.models import Status
# from apps.bridge.models import Manifest
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import BasePermission
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse


class CoreAPIView(GenericAPIView):
    # def dispatch(self, request, *args, **kwargs):
    #     self.third_party_flag = kwargs.get('thirdPartyFlag', 'N')
    #     return super().dispatch(request, *args, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.third_party_flag = 'N'
        self.success = True
        self.debug_flag = 'N'
        self.params = {}
        self.message = 'call successful'
        self.messages = []
        self.data = {}
        self.request_id = ''
        self.user_id = None
        self.access_user_id = None
        self.response_format = 'camel_case'

    def dispatch(self, request, *args, **kwargs):
        # Set third_party_flag before the view logic runs
        self.third_party_flag = kwargs.pop('thirdPartyFlag', 'N')
        return super().dispatch(request, *args, **kwargs)

    def get_response(self):
        response = self.build_response()

        if self.response_format == 'camel_case':
            # response = convert_to_camel_case(response)
            response = format_response(response)

        return Response(response)

    def build_response(self):
        status = 'success' if self.success else 'error'
        user_logged_in = self.user_id is not None
        response = {
            'status': status,
            'message': self.message,
            'meta': {
                'version': constants.VERSION,
                # '3flag': self.third_party_flag,
                'database_key': os.getenv('DATABASE_KEY'),
                # 'database-id':  os.getenv('DATABASE_ID'),
                # 'request-id': self.request_id,
                'parameters': self.params,
            },
            'header': {
                'user': {
                    'logged_in': user_logged_in
                }
            }
            # 'data': self.data
        }

        if len(self.messages) > 0:
            response['messages'] = self.messages

        return response

    def load_request(self, request):
        self.request_id = getattr(request, "request_id", "unknown")
        self.debug_flag = self.get_param('debugFlag', 'N', False)

        if hasattr(request.user, 'user_id'):
            self.user_id = request.user.user_id
        else:
            self.user_id = None  # or 'anonymous', or skip setting it

        self.access_user_id = self.user_id

    def get_param(self, key, default_value, required, parameter_type=None):
        ret_value = default_value
        params: Request = self.request.query_params

        if key in params:
            ret_value = params[key]

        if required and not ret_value:
            self.message = 'missing parameter(s)'
            self.add_message(f'missing parameter: {key}', success=False)

        if key != 'debugFlag':
            self.params[key] = ret_value

        if parameter_type and parameter_type == 'decimal':
            try:
                ret_value = Decimal(ret_value)
                self.params[key] = ret_value
            except InvalidOperation as e:
                self.add_message(f'{key} format error. expecting {parameter_type}:  {str(e)}', success=False)

        return ret_value

    def add_message(self, message, success=True):
        self.messages.append(message)
        self.success = self.success and success
        if not self.success:
            self.set_message('call failed')

    def set_message(self, message, success=True):
        self.messages.append(message)
        self.message = message
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
        self.set_message('get() not defined', success=False)

    def post_get(self, request):
        pass

    def post(self, request):
        try:
            self.load_request(request)
            # if self.status == 200:
            if self.success:
                self.pre_post(request)
                if self.success:
                    if self.success:
                        self._post(request)
                        if self.success:
                            self.post_post(request)
        except Exception as e:
            self.add_message(f'post error:  {str(e)}', success=False)

        return self.get_response()

    def pre_post(self, request):
        pass

    def _post(self, request):
        self.set_message('post() not defined', success=False)

    def post_post(self, request):
        pass

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


class AuthorizedAPIView(CoreAPIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_request(self, request):
        super().load_request(request)

        self.user_id = request.user.user_id


class PublicAPIView(CoreAPIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TestAPI(PublicAPIView):
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


class GuestRoomAPI(AuthorizedAPIView):
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

        # manifests = Manifest.objects.filter(
        # )
        # record1 = manifests[0]
        # self.data['Status'] = '001'
        # self.data['HotelId'] = record1.hotel.hotel_id
        # self.data['HotelName'] = record1.hotel.description
        # self.data['ReservationId'] = record1.res_identifier
        # self.data['ReservationStatus'] = record1.res_status_identifier
        # self.data['ChannelId'] = record1.channel_identifier
        # self.data['BookingPlatform'] = record1.booking_platform
        # self.data['CreatedDate'] = '2025-02-15'
        # self.data['CreatedTime'] = '09:12:34'
        # self.data['CheckInDate'] = record1.check_in_date
        # self.data['CheckOutDate'] = record1.check_out_date
        # self.data['CheckOutDate'] = record1.check_out_date
        # self.data['Pax'] = manifests.count()
        # self.data['PMSIRooms']: []

        # rooms = self.data['PMSIRooms'] = {
        #     'RoomNumber': record1.room_number,
        #     'RoomType': record1.room_type,
        #     'PMSIGuests': []
        # }
        # guests = rooms['PMSIGuests']
        #
        # for manifest in manifests:
        #     guests.append(
        #         {
        #             "GuestName": f"{manifest.first_name} {manifest.last_name}",
        #             "GuestId": manifest.guest_identifier,
        #             "FirstName": manifest.first_name,
        #             "LastName": manifest.last_name,
        #             "Email": manifest.email,
        #             "Gender": manifest.gender,
        #             "Birthday": manifest.birth_date,
        #             "Mobile": manifest.mobile_phone_number,
        #             "Nationality": manifest.nationality,
        #             "DocumentNumber": manifest.document_number,
        #             "DocumentType": manifest.document_type,
        #
        #         }
        #     )
        #
        # print(guests)


class IsThirdPartyUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='ThirdParty').exists()


class ThirdPartyAuthorizedAPIView(AuthorizedAPIView):
    permission_classes = AuthorizedAPIView.permission_classes + [IsThirdPartyUser]


def nest_record(record):
    nested = {}
    try:
        for key, value in record.items():
            # print(f'{key}:{value}')
            parts = key.split("__")
            current = nested
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
    except Exception as e:
        print(f'{str(e)}')
    return nested


def nest_records(records):
    return [nest_record(record) for record in records]


# def convert_to_camel_case(obj):
#     def snake_to_camel(s):
#         parts = s.split('_')
#         return parts[0] + ''.join(word.capitalize() for word in parts[1:])
#
#     new_obj = obj
#     if isinstance(obj, dict):
#         new_obj = {}
#         for k, v in obj.items():
#             new_key = snake_to_camel(k)
#             new_obj[new_key] = convert_to_camel_case(v)
#     elif isinstance(obj, list):
#         new_obj = [convert_to_camel_case(item) for item in obj]
#
#     return new_obj
#

def format_response(obj, level=0):
    def snake_to_camel(s):
        # return s
        parts = s.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    new_obj = obj
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            indent = ' -' * level
            # print(f'{indent} {k}')
            new_key = snake_to_camel(k)
            new_obj[new_key] = format_response(v, level+1)
    elif isinstance(obj, list):
        new_obj = []
        for item in obj:
            if isinstance(item, dict):
                item = nest_record(item)
            # print(f'{" -" * level} PROCESSING LIST ELEMENT: {item}')
            result = format_response(item, level + 1)
            new_obj.append(result)

    return new_obj



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


def health_check(request):
    return JsonResponse({'status': 'ok'})