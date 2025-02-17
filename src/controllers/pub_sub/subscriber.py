import threading
from google.cloud import pubsub_v1
from src.settings import GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME
from src.controllers.pub_sub.processes import locked_callback_example


class Subscriber:
    """
    Base class for the `Subscriber` class.
    This class create a connection to the Pub/Sub subscription, no action is taken on the connection,
    use the `SubscriberQueue` class to manage a queue, or create a new class for concurrent flows.

    Args:
    -----
        None

    Returns:
    -------
        None

    Usage example:
    --------------
    create e new class:
    ```
    class SubscriberConcurrent(Subscriber):
        . . .
    ```
    """
    __subscription_name__: str = f'projects/{GCP_PROJECT_ID}/subscriptions/{PUBSUB_SUBSCRIPTION_NAME}'
    subscriber = pubsub_v1.SubscriberClient()


class SubscriberQueue(Subscriber):
    """
    `SubscriberQueue` singleton class.
    This class create a connection to the Pub/Sub subscription, and queue receives messages from it.
    This class and methods are designed to be used in secuential flows, ensuring that only one message is processed at a time.

    Args:
    -----
        None

    Returns:
    -------
        None

    Usage example:
    --------------

    ```
        subscriber_queue = SubscriberQueue()
        subscriber_queue.run(callback=your_function)
    ```

    This functions uses the default subscription and GCP project ID. You can change them by setting the '__subscription_name__'
    according to your needs.
    """
    _instance = None
    _lock = threading.Lock()
    _run_instance_executed = False

    def __new__(cls, *args, **kwargs):
        """
        Create and return a singleton instance of the class.

        This method is used to create and return a singleton instance of the class.
        It ensures that only one instance of the class is created and used throughout the program.

        Parameters:
        -----------
            cls (type): The class object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
        --------

            cls._instance: The singleton instance of the class.
        """

        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    def run_instance(self, callback=locked_callback_example):
        """
        Run the instance by starting a new thread to call the start_pull method with the provided callback.

        Parameters:
        -----------
            callback: The function to be called when a message is received.

        Returns:
        --------
            None
        """
        with self._lock:
            if not self._run_instance_executed:
                pubsub_thread = threading.Thread(
                    target=self.start_pull,
                    name="pubsub_queue_instance",
                    kwargs={'callback': callback}
                )
                pubsub_thread.start()
                self._run_instance_executed = True
            else:
                print("run_instance already executed.")

    def start_pull(self, callback=locked_callback_example):
        """
        Start pulling messages from the Pub/Sub subscription using the provided callback function.

        Args:
            `callback` (function, optional): The callback function to be called when a message is received.
            Defaults to `locked_callback_example`.

        Returns:
            None
        """
        streaming_pull_future = self.subscriber.subscribe(
            self.__subscription_name__, callback=callback)
        print(f"Listening for messages on {self.__subscription_name__}...\n")
        try:
            streaming_pull_future.result()
        except Exception as error:
            print(f'PUB/SUB ERROR on pulling: {error}')
            streaming_pull_future.cancel()
        print("Done!")

    def run(self, callback=locked_callback_example):
        """
        Runs the instance by starting a new thread to call the `start_pull` method with the provided `callback`.

        Parameters:
        -----------
            `callback` (function, optional): The function to be called when a message is received.
                Defaults to `locked_callback_example`.

        Returns:
        --------
            None

        Prints:
            "Queue in execution..."
        """
        self.run_instance(callback)
        print("Queue in execution...")