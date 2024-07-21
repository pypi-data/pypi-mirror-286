from datetime import datetime, timedelta


def seconds_to_next_interval(dt: datetime, interval_seconds: int) -> float:
    # Calculate total minutes since midnight
    seconds_since_midnight = (dt.hour * 60 + dt.minute) * 60 + dt.second

    # Find the next multiple of the interval
    next_interval_second = ((seconds_since_midnight // interval_seconds) + 1) * interval_seconds

    # Calculate the time of the next interval
    next_interval_time = datetime(dt.year, dt.month, dt.day, 0, 0) + timedelta(seconds=next_interval_second)

    # Calculate the number of seconds until the next interval
    seconds_to_next = (next_interval_time - dt).total_seconds()

    return seconds_to_next


def is_midnight() -> bool:
    # Get the current local time
    now = datetime.now()

    # Get the hour component of the current time
    hour = now.hour

    return hour < 7


if __name__ == '__main__':
    print(seconds_to_next_interval(datetime.now(), 3600 * 12))
    print(is_midnight())
