from django.db.models import F, Value as V, Case, When
from django.db.models.functions import Concat


class PersonUtilities:
    @staticmethod
    def get_full_name(first='', middle='', last='', salutation=''):
        first = first or ''
        middle = middle or ''
        last = last or ''
        salutation = salutation or ''

        suffix = ' '.join(
            p.strip() for p in [middle, salutation] if p
        )

        full_name = f'{last}, {first}'

        if suffix:
            full_name = f'{full_name} {suffix}'

        return full_name
    # def get_full_name(first, middle, last, salutation):
    #     full_name = f'{last}, {first}' + ' '.join(p.strip() for p in [middle, salutation] if p)
    #     return full_name


def get_person_name(prefix='', name_format='L/F (C)'):
    person_id = F(f'{prefix}__person_id')
    fields_map = {
        'L': F(f'{prefix}__last_name'),
        'F': F(f'{prefix}__first_name'),
        'C': F(f'{prefix}__code')
    }

    parts = []
    for char in name_format:
        if char in fields_map:
            parts.append(fields_map[char])
        else:
            parts.append(V(char))

    name = Concat(*parts)
    name = Case(
        When(**{f'{prefix}__person_id': 'A9999'}, then=V('TBA')),
        default=name
    )

    return name
