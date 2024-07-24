import socket
from inspect import isfunction, iscoroutinefunction
from typing import List, Dict, Any, Literal, Callable

HOST_TYPE = Literal['local', 'public']


def get_host(host_type: HOST_TYPE = 'local') -> str:
    import httpx

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


def find_process_pids_by_process_name(process_name: str) -> List[int]:
    import psutil

    process_pids: List[int] = []
    for proc in psutil.process_iter(['pid', 'name']):
        proc_info: Dict[str, Any] = proc.info  # type: ignore
        try:
            if process_name.lower() in proc_info['name'].lower():
                process_pids.append(proc_info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_pids


def kill_process_by_process_pid(process_pid: int) -> None:
    import psutil

    try:
        proc = psutil.Process(process_pid)
        proc.terminate()
        proc.wait(timeout=3)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
        pass


def kill_process_by_process_name(process_name: str) -> None:
    process_pids = find_process_pids_by_process_name(process_name)
    for process_pid in process_pids:
        kill_process_by_process_pid(process_pid)
