from abc import ABC, abstractmethod
from typing import Any, Callable


class DataBus(ABC):
    """
    A Databus Interface class to handle both async messaging and synchronous messaging.
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def make_connection(self):
        """
        Connect to the Databus server.
        """
        pass

    @abstractmethod
    def close_connection(self):
        """
        Close connection from the Databus server.
        """
        pass

    @abstractmethod
    def publish_event(self, topic: str, event_payload: dict):
        """
        Publish an async message to a Databus topic.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.
        """
        pass

    @abstractmethod
    def request_event(self, topic, event_payload):
        """
        Send a synchronous request/message to a Databus topic and recieve response.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.

        Returns:
            response (Any): response message
        """
        pass

    @abstractmethod
    def subscribe_sync_event(self, topic, callback: Callable[[Any], None]):
        """
        Subscribe to a databus topic and process messages synchronously.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
        """
        pass

    @abstractmethod
    def subscribe_async_event(self, topic, callback: Callable[[Any], None]):
        """
        Subscribe to a databus topic and process messages asynchronously.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
        """
        pass
