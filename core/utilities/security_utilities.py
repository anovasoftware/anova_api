from apps.base.models import RoleItem, UserRole
from constants import status_constants

class SecurityUtility:
    @staticmethod
    def user_can_charge_item(user, item) -> bool:

        role_items = RoleItem.objects.filter(
            role__userRoles__user=user.pk,
            item_id=item.item_id,
            allow_api_charge=True,
            status=status_constants.ACTIVE
        )
        can_charge = role_items.exists()
        return can_charge