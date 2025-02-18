import random
import threading
from time import sleep
from datetime import datetime
from src.services.deepseek.interface import DeepSeek
from src.connectors.long_process.async_process import AsyncProcess

__LOCK__ = threading.Lock()

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
    """
    Executes the core logic of the async process callback.

    This function acquires a lock and checks if the message data exists in the AsyncProcess table.
    If the record exists, it updates the status to 'successful' and the output field with a success message.
    It then sleeps for 10 seconds and acknowledges the message.

    Args:
    -----
        message (Message): The message to be processed.

    Returns:
    -------
        None
    """
    with __LOCK__:
        data = message.data.decode("utf-8")
        ap = AsyncProcess()
        job = ap.custom_filter(where_dict={'id': data.encode()})
        if job:
            job = job[0]
            output = DeepSeek().generate(job['input'])
            ap.update_by_filter(
                filter_criteria={'id': job['id']},
                update_values={
                    'status': ap.__successful__,
                    'output': output.json(),
                    }
                )
        message.ack()
