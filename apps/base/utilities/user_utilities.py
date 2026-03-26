from apps.base.serializers.user import UserSerializer
from apps.base.serializers.role import RoleSerializer
from apps.static.serializers.client import ClientSerializer
from apps.static.serializers.hotel import HotelSerializer
from apps.static.serializers.menu import MenuSerializer
from apps.static.models import Client, Hotel, Menu
from apps.base.models import UserHotel, RoleMenu, UserRole, Role
from constants import hotel_constants, status_constants


def get_user_profile(user, is_logged_in=False):
    user_id = user.user_id

    roles = get_roles(user_id)
    menus = get_menus(roles)

    client_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel__client_id', flat=True)
    clients = Client.objects.filter(client_id__in=client_ids).order_by('description')

    hotel_ids = UserHotel.objects.filter(user_id=user_id).values_list('hotel_id', flat=True)
    hotels = Hotel.objects.filter(hotel_id__in=hotel_ids).order_by('description')

    if hotels.exists() and user.last_hotel_id == hotel_constants.NOT_APPLICABLE:
        user.last_hotel_id = hotels.first().hotel_id
        user.save()

    profile = UserSerializer(user).data
    profile['is_logged_in'] = is_logged_in
    profile['hotels'] = HotelSerializer(hotels, many=True).data
    profile['clients'] = ClientSerializer(clients, many=True).data
    profile['roles'] = RoleSerializer(roles, many=True).data
    profile['menus'] = MenuSerializer(menus, many=True).data

    return profile

def get_roles(user_id):
    role_ids = UserRole.objects.filter(
        user_id=user_id,
        effective_status=status_constants.EFFECTIVE_STATUS_CURRENT
    ).values_list(
        'role_id', flat=True
    ).distinct()

    role_ids = list(role_ids)
    roles = Role.objects.filter(role_id__in=role_ids).order_by('description')

    return roles


def get_menus(roles):
    role_ids = roles.values_list('role_id', flat=True)
    role_ids = list(role_ids)
    menu_ids = RoleMenu.objects.filter(
        role_id__in=role_ids,
        effective_status=status_constants.EFFECTIVE_STATUS_CURRENT
    ).values_list('menu_id', flat=True)

    menus = Menu.objects.filter(menu_id__in=menu_ids).order_by('description')

    return menus