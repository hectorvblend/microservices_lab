from typing import Optional
from google.cloud import pubsub_v1
from src.settings import GCP_PROJECT_ID, PUBSUB_TOPIC_NAME


class Publisher:
    """
    Base class for the `Publisher` class.
    This class create a connection to the Pub/Sub topic, and publishes messages to it.

    Args:
    -----
        None

    Returns:
    -------
        None

    Usage example:
    --------------
    ```
        publisher = Publisher()
        publisher.create_topic()
        publisher.publish_message("Hello, World!")
    ```
    """
    __topic_name__: str = f'projects/{GCP_PROJECT_ID}/topics/{PUBSUB_TOPIC_NAME}'
    publisher = pubsub_v1.PublisherClient()

    def create_topic(self, topic_name: str = __topic_name__):
        """
        Creates a topic with the given name using the PublisherClient.

        Args:
        -----
            `topic_name` (str): The name of the topic to be created. Defaults to the predefined topic name.

        Returns:
        -------
            None
        """
        self.publisher.create_topic(name=topic_name)

    def publish_message(self, message: Optional[str]):
        """
        A function to publish a message to a topic.

        Args:
        -----
            `message` (str): The message to be published.

        Returns:
        -------
            None
        """
        if message is None:
            raise ValueError("Message cannot be None")
        future = self.publisher.publish(self.__topic_name__, message.encode())
        future.result()