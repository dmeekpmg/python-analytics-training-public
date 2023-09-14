from datetime import datetime, timedelta
import sched, time
from typing import Sequence

from data import realtime


START_HOUR = 8
START_MINUTE = 0


def generate_fetch_times(start_time=datetime.now(), wait_time=60, max_iters=60):
    """Generator function to calculate the next refresh time. We use
    this rather than just waiting 60 seconds so that we can get exactly
    60 requests in one hour and not be affected by the time taken to
    extract and save results.

    Args:
        start_time (_type_, optional): _description_. Defaults to datetime.now().
        wait_time (int, optional): _description_. Defaults to 60.
        max_iters (int, optional): _description_. Defaults to 60.

    Yields:
        _type_: _description_
    """
    next_time = start_time
    max_time = start_time + timedelta(0, max_iters * wait_time)
    while next_time < max_time:
        # If the time is in the past (e.g. we started the process late),
        # then jump to the next minute
        while next_time < datetime.now():
            next_time += timedelta(0, wait_time)

        yield next_time.timestamp()
        next_time += timedelta(0, wait_time)


def schedule_fetch(scheduler:sched.scheduler, fetch_times:Sequence): 
    # schedule the next call first
    scheduler.enterabs(
        next(fetch_times), 
        1, 
        schedule_fetch, 
        (scheduler,fetch_times)
    )
    try:
        realtime.fetch_and_upload_positions()
    except:
        print(f"Fetching failed: {datetime.now()}")
    # then do your stuff


def main():
    # Generate times for today
    now = datetime.now()
    today = (now.year, now.month, now.day)
    fetch_times = generate_fetch_times(
        datetime(*today, START_HOUR, START_MINUTE), 
        60
    )

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(
        next(fetch_times), 
        1, 
        schedule_fetch, 
        (scheduler, fetch_times)
    )
    scheduler.run()


if __name__ == "__main__":
    main()