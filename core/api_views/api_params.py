from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional

def _to_str(v):
    if v is None:
        return None
    return str(v).strip()

@dataclass(frozen=True)
class ParamSpec:
    name: str                    # external name: 'typeId'
    dest: str                    # internal attr: 'type_id'
    kind: str                    # 'query' or 'body' or 'either'
    cast: Callable[[Any], Any]   # str -> int, str -> str, etc
    required_get: bool = False
    required_post: bool = False
    required_patch: bool = False
    description: str = ''
    default: Any = None
    allowed: Optional[Iterable[Any]] = None   # list/tuple/set or callable later

def with_allowed(spec: ParamSpec, allowed):
    return ParamSpec(**{**spec.__dict__, 'allowed': allowed})

COMMON_PARAMS = {
    'debugFlag': ParamSpec(
        name='debugFlag',
        dest='debug_flag',
        kind='query',
        cast=bool,
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
    'itemId': ParamSpec(
        name='itemId',
        dest='item_id',
        kind='either',
        cast=_to_str,
        description='Hotel id for the request.',
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
