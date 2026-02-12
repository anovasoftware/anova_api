from rest_framework import serializers as s
from drf_spectacular.utils import inline_serializer
from core.utilities.string_utilities import snake_to_camel

MetaSerializer = inline_serializer(
    name='Meta',
    fields={
        'version': s.CharField(help_text='API version (e.g., 03.01.08)'),
        'databaseKey': s.CharField(help_text='Database key (e.g., production)'),
        'parameters': s.DictField(
            help_text='Original request parameters.'
        ),
        'recordCount': s.IntegerField(help_text='Number of records returned'),
    },
)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For may be a comma-separated list of IPs
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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


def flat_record(record: dict) -> dict:
    flat = {}

    def _flatten(prefix, value):
        if isinstance(value, dict):
            for k, v in value.items():
                _flatten(f'{prefix}__{k}' if prefix else k, v)
        else:
            flat[prefix] = value

    _flatten('', record)
    # Replace double underscores with single underscores
    return {k.replace('__', '_'): v for k, v in flat.items()}


def transform_records(records, shape='nested'):
    # return [nest_record(record) for record in records]
    if shape == 'flat':
        records_adjusted = [flat_record(record) for record in records]
    else:
        records_adjusted = [nest_record(record) for record in records]

    return records_adjusted


def format_response(obj, level=0):
    # def snake_to_camel(s):
    #     # return s
    #     parts = s.split('_')
    #     return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    new_obj = obj
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            indent = ' -' * level
            # print(f'{indent} {k}')
            new_key = snake_to_camel(k)
            new_obj[new_key] = format_response(v, level + 1)
    elif isinstance(obj, list):
        new_obj = []
        for item in obj:
            if isinstance(item, dict):
                item = nest_record(item)
            # print(f'{" -" * level} PROCESSING LIST ELEMENT: {item}')
            result = format_response(item, level + 1)
            new_obj.append(result)

    return new_obj
