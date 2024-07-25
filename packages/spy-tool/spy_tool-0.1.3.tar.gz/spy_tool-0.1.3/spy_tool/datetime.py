import datetime


def now() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def date_delta(start_time: str, end_time: str) -> int:
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    time_diff = end_time - start_time
    seconds = time_diff.total_seconds()
    return int(seconds)
