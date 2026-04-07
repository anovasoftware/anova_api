from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional
from decimal import Decimal, ROUND_HALF_UP


def _to_str(v):
    if v is None:
        return None
    return str(v).strip()


def _to_yn(v):
    if v is None:
        return None
    v = str(v).strip().upper()
    if v not in ('Y', 'N'):
        raise ValueError('Expected Y or N')
    return v


def _to_money(v):
    if v is None or v == '':
        return None
    try:
        d = Decimal(str(v).strip())
        return d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except Exception:
        raise ValueError(f'Invalid money value: {v}')


@dataclass(frozen=True)
class ParamSpec:
    name: str  # external name: 'typeId'
    dest: str  # internal attr: 'type_id'
    kind: str  # 'query' or 'body' or 'either'
    cast: Callable[[Any], Any]  # str -> int, str -> str, etc
    required_get: bool = False
    required_post: bool = False
    required_patch: bool = False
    description: str = ''
    default: Any = None
    allowed: Optional[Iterable[Any]] = None  # list/tuple/set or callable later


def with_allowed(spec: ParamSpec, allowed):
    return ParamSpec(**{**spec.__dict__, 'allowed': allowed})


COMMON_PARAMS = {
    'action': ParamSpec(
        name='action',
        dest='action',
        kind='either',
        cast=_to_str,
        description='Action.',
    ),
    'amount': ParamSpec(
        name='amount',
        dest='amount',
        kind='either',
        cast=_to_money,
        description='Amount.',
    ),
    'debugFlag': ParamSpec(
        name='debugFlag',
        dest='debug_flag',
        kind='query',
        cast=_to_yn,
        default='N',
        description='Enable debug output.',
        allowed=('Y', 'N'),
    ),
    'guestId': ParamSpec(
        name='guestId',
        dest='guest_id',
        kind='either',
        cast=_to_str,
        description='Guest id for the request.',
        allowed=None,
    ),
    'hotelId': ParamSpec(
        name='hotelId',
        dest='hotel_id',
        kind='either',
        cast=_to_str,
        description='Hotel id for the request.',
    ),
    'hotelPublicKey': ParamSpec(
        name='hotelPublicKey',
        dest='hotel_public_key',
        kind='either',
        cast=_to_str,
        description='Hotel public key for the request.',
    ),
    'itemId': ParamSpec(
        name='itemId',
        dest='item_id',
        kind='either',
        cast=_to_str,
        description='Item id for the request.',
    ),
    'rfidUid': ParamSpec(
        name='rfidUid',
        dest='rfid_uid',
        kind='query',
        cast=_to_str,
        description='RFID UID)',
    ),
    'roomCode': ParamSpec(
        name='roomCode',
        dest='room_code',
        kind='query',
        cast=_to_str,
        description='Room/cabin code (e.g., 101).',
    ),
    'searchString': ParamSpec(
        name='searchString',
        dest='search_string',
        kind='query',
        cast=_to_str,
        description='Search string (e.g., Johnson).',
    ),
    'shape': ParamSpec(
        name='shape',
        dest='result_shape',
        kind='query',
        cast=_to_str,
        default='nested',
        allowed=('nested', 'flat'),
        description='Result shape. (nested or flat)',
    ),
    'statusId': ParamSpec(
        name='statusId',
        dest='status_id',
        kind='either',
        cast=_to_str,
        description='Status id for the request.',
        allowed=None,
    ),
    'postingType': ParamSpec(
        name='postingType',
        dest='posting_type',
        kind='either',
        cast=_to_str,
        description='Posting type (batch or simple).',
        allowed=('batch', 'simple', 'detail'),
    ),
    'recordId': ParamSpec(
        name='recordId',
        dest='record_id',
        kind='either',
        cast=_to_str,
        description='Record id for the request.',
        allowed=None,
    ),
    'typeId': ParamSpec(
        name='typeId',
        dest='type_id',
        kind='either',
        cast=_to_str,
        description='Type id for the request.',
        allowed=None,
    ),

}

TRANSACTION_PARAMS = {
    'externalReference': ParamSpec(
        name='externalReference',
        dest='external_reference',
        kind='either',
        cast=_to_str,
        description='External transaction reference.',
    ),
    'externalAuthorizationCode': ParamSpec(
        name='externalAuthorizationCode',
        dest='external_authorization_code',
        kind='either',
        cast=_to_str,
        description='External authorization code.',
    ),
}

PARAM_DEFINITIONS = {
    **COMMON_PARAMS,
    **TRANSACTION_PARAMS,
}
