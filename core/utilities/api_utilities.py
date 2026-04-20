from rest_framework import serializers as s
from drf_spectacular.utils import inline_serializer

MetaSerializer = inline_serializer(
    name='Meta',
    fields={
        'version': s.CharField(help_text='API version (e.g., 03.01.08)'),
        # 'databaseKey': s.CharField(help_text='Database key (e.g., production)'),
        'parameters': s.DictField(
            help_text='Original request parameters.'
        ),
        # 'recordCount': s.IntegerField(help_text='Number of records returned'),
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

def process_supports_method(process, method: str) -> bool:
    supported = False
    method = (method or '').upper()
    if method in ('HEAD', 'OPTIONS'):
        supported = True
    if method == 'GET':
        supported = getattr(process, 'supports_read', True)
    if method == 'POST':
        supported = getattr(process, 'supports_create', False)
    if method in ('PUT', 'PATCH'):
        supported = getattr(process, 'supports_update', False)
    if method == 'DELETE':
        supported = getattr(process, 'supports_delete', False)

    return supported

def required_flag_for_method(request_method: str) -> str | None:
    flag = None
    method = (request_method or '').upper()
    if method in ('GET', 'HEAD', 'OPTIONS'):
        flag = 'can_read'
    if method == 'POST':
        flag = 'can_create'
    if method in ('PUT', 'PATCH'):
        flag = 'can_update'
    if method == 'DELETE':
        flag = 'can_delete'

    return flag


def model_to_field_dict(obj, fields):
    result = {}
    for field in fields:
        value = obj
        for part in field.split('__'):
            value = getattr(value, part)
        result[field] = value
    return result
