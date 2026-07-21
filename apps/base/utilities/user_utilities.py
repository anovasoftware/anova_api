from apps.base.serializers.user import UserSerializer
from apps.base.serializers.role import RoleSerializer
from apps.base.utilities.hotel_utilities import get_hotel_extension
from apps.static.serializers.client import ClientListSerializer, ClientDetailSerializer
from apps.static.serializers.hotel import HotelDetailSerializer, HotelListSerializer
from apps.static.serializers.menu import MenuSerializer
from apps.static.models import Client, Hotel, Menu
from apps.base.models import UserHotel, RoleMenu, UserRole, Role
from apps.static.utilities.client_utilities import get_client_extension
from constants import hotel_constants, status_constants, role_constants, type_constants


def get_user_profile(user, is_logged_in=False):
    user_id = user.user_id

    hotel_ids = UserHotel.objects.filter(
        user_id=user_id,
        status_id=status_constants.ACTIVE
    ).values_list(
        'hotel_id', flat=True
    )
    hotels = Hotel.objects.filter(
        status_id=status_constants.ACTIVE,
        hotel_id__in=hotel_ids
    ).order_by(
        'description'
    )

    if hotels.exists() and user.last_hotel_id == hotel_constants.NOT_APPLICABLE:
        user.last_hotel_id = hotels.first().hotel_id
        user.save()

    current_hotel = hotels.filter(hotel_id=user.last_hotel_id).first()
    current_client = (current_hotel.client if current_hotel else None )
    current_hotel_extension = get_hotel_extension(user.last_hotel_id)
    current_client_extension = get_client_extension(current_hotel.client_id)

    client_ids = UserHotel.objects.filter(
        user_id=user_id,
        status_id=status_constants.ACTIVE
    ).values_list(
        'hotel__client_id', flat=True
    )
    clients = Client.objects.filter(client_id__in=client_ids).order_by('description')

    roles = get_roles(user_id, user.last_hotel_id)
    menus = get_menus(roles)

    profile = UserSerializer(user).data
    profile['is_logged_in'] = is_logged_in
    profile['current_hotel'] = (HotelDetailSerializer(current_hotel).data if current_hotel else None)
    profile['current_client'] = (ClientDetailSerializer(current_client).data if current_client else None)
    profile['hotels'] = HotelListSerializer(hotels, many=True).data
    profile['clients'] = ClientListSerializer(clients, many=True).data
    profile['roles'] = RoleSerializer(roles, many=True).data
    profile['menus'] = MenuSerializer(menus, many=True).data

    return profile



def get_roles(user_id, hotel_id=None):
    user_roles = UserRole.objects.filter(
        user_id=user_id,
        effective_status=status_constants.EFFECTIVE_STATUS_CURRENT,
    )

    roles = Role.objects.exclude(
        type_id=type_constants.NOT_APPLICABLE
    )

    if not user_roles.filter(
            role_id=role_constants.SYSTEM_ADMINISTRATOR
    ).exists():
        roles = roles.filter(
            role_id__in=user_roles.values('role_id')
        )

    hotel_ids = [hotel_constants.NOT_APPLICABLE]

    if hotel_id not in hotel_ids:
        hotel_ids.append(hotel_id)

    roles = roles.filter(
        hotel_id__in=hotel_ids
    ).order_by(
        'role_id'
    )

    return roles


def get_menus(roles):
    role_ids = roles.values('role_id')

    menu_ids = RoleMenu.objects.filter(
        role_id__in=role_ids,
        effective_status=status_constants.EFFECTIVE_STATUS_CURRENT,
    ).values(
        'menu_id'
    )

    menus = Menu.objects.filter(
        menu_id__in=menu_ids
    ).distinct(
    ).order_by(
        'order_by'
    )
    return menus
