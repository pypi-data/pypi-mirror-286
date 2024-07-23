import re
import hashlib
from typing import Optional, Any, List, Dict, Literal


def camel_to_snake(name: str) -> str:
    """
    >>> camel_to_snake('CamelCaseString')
    'camel_case_string'

    :param name:
    :return:
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


ALGO_TYPE = Literal[
    'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384',
    'sha3_512', 'shake_128', 'shake_256'
]


def gen_uxid(
        *args: Any,
        keys: Optional[List] = None, item: Optional[Dict] = None,
        algo_type: ALGO_TYPE = 'md5'
) -> str:
    """
    >>> gen_uxid('123456')
    'e10adc3949ba59abbe56e057f20f883e'

    :param args:
    :param keys:
    :param item:
    :param algo_type:
    :return:
    """
    m = hashlib.new(algo_type)
    if args:
        values = args
    elif keys is not None and item is not None:
        if isinstance(keys, list) and isinstance(item, dict):
            values = [item[k] for k in keys if k in item]
        else:
            raise ValueError('Keys and item must be list and dict!')
    elif item is not None:
        values = [item[k] for k in sorted(item.keys())]
    else:
        raise ValueError('Args or keys and item or item must be provided!')

    data = list(map(lambda x: str(x), values))

    for i in data:
        m.update(i.encode())

    return m.hexdigest()
