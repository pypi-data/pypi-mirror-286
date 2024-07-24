from types import NoneType

TYPE_LOOKUP = {
    bool: 'bool',
    bytes: 'bytes',
    float: 'float',
    int: 'int',
    list: 'list',
    dict: 'map',
    str: 'string',
    NoneType: 'null',
}


def get_type(el):
    try:
        return TYPE_LOOKUP[type(el)]
    except KeyError:
        raise ValueError(f'Unknown type {type(el)}')


helpers = {
    # CONVERSION
    'double': float,
    'int': int,
    'string': str,
    # DATA TYPE
    'keys': lambda collection: list(collection.keys()),
    'len': len,
    'set': set,  # unsure if this is valid in the actual GC workflows
    # CONDITIONAL
    'default': lambda some, default: some or default,
    'if': lambda cond, if_true, if_false: if_true if cond else if_false,
    # TYPE
    'get_type': get_type,
    'not': lambda some: not some,
}
