import base64
import random
import threading
from time import sleep
from datetime import datetime, timezone
from src.settings import WATCHDOG_MONITOR_INTERVAL_SEC
from src.controllers.pub_sub.publisher import Publisher
from src.connector.sql_alchemy.ap.async_process import AsyncProcess

__LOCK__ = threading.Lock()
__WATCHDOG_LOCK__ = threading.Lock()

def log_execution(save_to_file=False):
    """
    This function is a decorator that logs the start and end of the wrapped function along with its data.
    It takes a boolean argument `save_to_file` to specify whether the logs should be saved to a file.
    The `funcion` parameter is the function being wrapped.
    The `wrapper` function logs the start time, executes the wrapped function, logs the end time, and returns the result.

    Args:
        save_to_file (bool): Whether to save the logs to a file. Defaults to False.

    Returns:
        The result of the wrapped function.

    Example:
        >>> @log_execution
        ... def function(data):
        ...     return data
        ...
        >>> function("Hello World")
    """
    def decorator(funcion):
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"T: {timestamp} - (Start) - Data: {args}\n"
            print(log_message)

            if save_to_file:
                with open("callback_log.txt", "a") as f:
                    f.write(log_message)

            result = funcion(*args, **kwargs)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"T: {timestamp} - (End) - Data: {args}\n"
            if save_to_file:
                with open("callback_log.txt", "a") as f:
                    f.write(log_message)
            print(log_message)

            return result
        return wrapper
    return decorator


def locked_callback_example(message):
    """
    Executes a callback function with a lock to ensure thread safety.

    Args:
    -----
        message (Message): The message to be processed.

    Returns:
    -------
        None

    This function acquires a lock before executing the callback function. 
    It decodes the message data, generates a random delay, sleeps for that amount of time,
    prints the decoded data and the delay, and acknowledges the message.
    """
    with __LOCK__:
        data = message.data.decode("utf-8")
        delay = random.randint(1, 4)
        sleep(delay)
        print(f"Data: {data} - locked_callback_example() - Delay: {delay} ")
        message.ack()

@log_execution()
def async_process_core_callback(message):
    with __LOCK__:
        data = message.data.decode("utf-8")
        ap = AsyncProcess()
        job = ap.custom_filter(where_dict={'id': base64.b64decode(data.encode())})
        if job and isinstance(job[0], dict) and job[0].get('event_type', False):
            job = job[0]
            if 'bp' in job['event_type'].lower():
                s = ScenarioMaster()
                s.execute_job(id=data)
        message.ack()

@log_execution()
def watchdog_monitor():
    """
    watchdog_monitor function that starts a watchdog monitor in a separate thread.
    The watchdog monitor continuously checks for missing jobs in the `ScenarioJobStatus`
    table and publishes them to a message queue.

    The function creates a nested function `watch()` that runs in a loop. Inside the loop, it performs the following steps:
    1. Creates an instance of the `ScenarioJobStatus` class.
    2. Retrieves a list of missing jobs from the `ScenarioJobStatus` table.
    3. Gets the current timestamp.
    4. Prints a message indicating the start of the watchdog monitor execution.
    5. If there are missing jobs, it creates an instance of the `Publisher` class and publishes each missing job's ID to the message queue.
    6. Updates the status and timestamp of the missing jobs in the `ScenarioJobStatus` table.
    7. Prints a message indicating the end of the watchdog monitor execution and the number of jobs rescheduled.
    8. Handles any exceptions that occur during the execution.
    9. Sleeps for a specified interval before repeating the loop.

    The function then creates a new thread using the `watch()` function as the target and starts the thread.
    """
    def watch():
        """
        Function to continuously monitor for missing jobs in the ScenarioJobStatus table and publish them to a message queue.

        Returns:

            None
        """
        get_timestamp = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Use a lock to ensure thread safety:
        with __WATCHDOG_LOCK__:
            while True:
                try:
                    print(f'T: {get_timestamp()} - watchdog_monitor execution begins')
                    # Get the current missing jobs:
                    ap = AsyncProcess()
                    IDs = ap.get_missing_or_failed_jobs()
                    # Update the status and timestamp of the missing jobs to put them in the queue:
                    if IDs:
                        pb = Publisher()
                        for ID in IDs:
                            id = ID['id']
                            ap.update_by_filter(
                                filter_criteria={'id':  base64.b64decode(id)},
                                update_values={
                                    'status': ap.__pending__,
                                    'updated_timestamp_utc': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
                                    })
                            pb.publish_message(message=id.decode())
                        print(f'T: {get_timestamp()} - watchdog_monitor execution begins')
                    print(f'T: {get_timestamp()} - watchdog_monitor execution ends, jobs rescheduled: {IDs}')
                except Exception as e:
                    print(f'Exception in watchdog_monitor() - {e} - T: {get_timestamp()}')
                sleep(WATCHDOG_MONITOR_INTERVAL_SEC)
    # Start the thread using the watch function:
    thread = threading.Thread(target=watch, name="watchdog_monitor")
    thread.start()