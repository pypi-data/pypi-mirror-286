from inspect import isfunction, iscoroutinefunction
from typing import List, Any, Literal, Callable

HOST_TYPE = Literal['local', 'public']


def get_host(host_type: HOST_TYPE = 'local') -> str:
    import socket
    import httpx  # type:ignore

    if host_type == 'local':
        return socket.gethostbyname(socket.gethostname())
    elif host_type == 'public':
        return httpx.get('https://api.ipify.org').text
    else:
        raise ValueError('Unsupported host_type!')


def chunk_data(data: List[Any], chunk_size: int) -> List[List[Any]]:
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


async def call_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    if not isfunction(func):
        raise ValueError('Unsupported func!')
    if iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)
