import time
import socket
from inspect import isfunction, iscoroutinefunction
from typing import List, Dict, Any, Literal, Callable, Protocol
from spy_tool.logger import logger

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
                proc_id = proc_info['pid']
                proc_name = proc_info['name']
                process_pids.append(proc_id)
                logger.success(f'Success find process_pid: {proc_id} proc_name: {proc_name}.')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as exception:
            logger.success(f'Fail find process_name: {process_name}, exception: {exception}!')
    logger.success(f'Found process_pids: {process_pids}.')
    return process_pids


def kill_process_by_process_pid(process_pid: int) -> None:
    import psutil

    try:
        proc = psutil.Process(process_pid)
        proc.terminate()
        proc.wait(timeout=3)
        logger.success(f'Success kill process_pid: {process_pid}.')
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as exception:
        logger.error(f"Fail kill process_pid: {process_pid}, exception: {exception}!")


def kill_process_by_process_name(process_name: str) -> None:
    process_pids = find_process_pids_by_process_name(process_name)
    for process_pid in process_pids:
        kill_process_by_process_pid(process_pid)


class Container(Protocol):
    def __init__(self, database, key):
        self.database = database
        self.key = key

    def __len__(self) -> int:
        pass


def show_progress(container: Container, frequency: float = 1.0) -> None:
    import tqdm

    total_num = len(container)
    desc = f"{container.database} {container.key} 消费速度"
    unit = "条"

    bar = tqdm.tqdm(desc=desc, total=total_num, leave=True, unit=unit)

    sum_num = 0
    while True:
        now_num = len(container)
        pass_num = total_num - now_num
        update_num = pass_num - sum_num
        sum_num += update_num

        bar.update(update_num)

        if sum_num == total_num:
            break

        time.sleep(frequency)
