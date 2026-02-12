import logging
from django.apps import apps
from django.utils import timezone
from django.db import transaction
from django.db import models

logger = logging.getLogger(__name__)


def get_next_id(identifier_id, length):
    next_id = None
    try:
        model = apps.get_app_config('base').get_model('Identifier')

        with transaction.atomic():
            identifier, _ = model.objects.select_for_update().get_or_create(identifier_id=identifier_id)
            identifier.last_identifier += 1
            identifier.last_updated = timezone.now()
            identifier.save()

        next_id = integer_to_char31(identifier.last_identifier, length)

    except Exception as e:
        logger.error(f"Error getting next ID for identifier {identifier_id}: {e}")

    return next_id


def integer_to_char31(int_value, length):
    mask = '0123456789BCDFGHJKLMNPQRSTVWXYZ'
    char_list = []

    for i in range(length, 0, -1):
        factor = 31 ** (i - 1)
        position = int_value // factor
        char_list.append(mask[position])
        int_value %= factor  # Reduce the value for the next iteration

    return ''.join(char_list).zfill(length)  # Ensure correct length


def get_active_dict(model: models.Model, record0: dict(), base_fields=False):
    record = dict()

    for key in record0:
        try:
            field = model._meta.get_field(key)
            if not base_fields or key == field.column:
                record[key] = record0[key]
        except Exception as e:
            continue

    return record


class ModelUtilities:
    @staticmethod
    def get_full_name(first, middle, last, salutation):
        full_name = f'{last}, {first}' + ' '.join(p.strip() for p in [middle, salutation] if p)
        return full_name
