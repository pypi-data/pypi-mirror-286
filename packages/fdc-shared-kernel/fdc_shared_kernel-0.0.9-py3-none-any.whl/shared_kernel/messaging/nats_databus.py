import json
import logging
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig, DeliverPolicy, StreamConfig
from typing import Callable, Any, List, Union
from shared_kernel.interfaces import DataBus


class NATSDataBus(DataBus):
    """
    A NATS Interface class to handle both standard NATS and JetStream operations.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NATSDataBus, cls).__new__(cls)
        return cls._instance

    def __init__(self, servers: str = None):
        """
        Initialize the NATSInterface.

        Args:
            servers (str): A string containing the NATS server URLs.
        """
        if not hasattr(self, "initialized"):  # to prevent reinitialization
            super().__init__()
            self.nc = NATS()
            self.servers = servers
            self.connected = False
            self.js = None  # JetStream context
            self.initialized = True

    async def make_connection(self):
        """
        Connect to the NATS server.
        """
        if not self.connected:
            await self.nc.connect(servers=self.servers)
            self.js = self.nc.jetstream(timeout=10)
            self.connected = True

    async def close_connection(self):
        """
        Close the connection to the NATS server.
        """
        try:
            if self.connected:
                await self.nc.close()
                self.connected = False
        except Exception as e:
            raise e

    async def create_stream(self, topics: List[Any]):
        """
        Create a stream for topics to persist the messages

        Args:
            topics (List): The messages in this topic with be persisted.
        """
        try:
            stream_name = "sample-stream-1"
            stream_config = StreamConfig(
                name=stream_name,
                subjects=topics,
                max_age=600,  # retain messages for 10 mins
            )
            await self.js.add_stream(stream_config)
        except Exception as e:
            raise e

    async def publish_event(
        self, topic: str, event_payload: dict
    ) -> Union[bool, Exception]:
        """
        Publish a message to a JetStream subject.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.

        Returns:
            bool: True if the event was published successfully.
        """
        try:

            ack = await self.js.publish(
                topic, json.dumps(event_payload).encode("utf-8")
            )
            logging.info(
                f"Published event '{event_payload.get('event_name')}' to topic '{topic}', ack: {ack}"
            )
            return True
        except Exception as e:
            logging.error(
                f"Failed to publish event '{event_payload.get('event_name')}': {str(e)}",
                exc_info=True,
            )
            raise e

    async def request_event(
        self, topic: str, event_payload: str, timeout: float = 10.0
    ) -> Union[dict, Exception]:
        """
        Send a request and wait for a response.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.
            timeout (float): The timeout for the request.

        Returns:
            dict: The response message.
        """
        try:
            response = await self.nc.request(
                topic, json.dumps(event_payload).encode("utf-8"), timeout=timeout
            )
            return json.loads(response.data.decode("utf-8"))
        except Exception as e:
            logging.error(f"Failed to request topic '{topic}': {e}", exc_info=True)
            raise e

    async def subscribe_async_event(
        self, topic: str, callback: Callable[[Any], None], durable_name: str
    ):
        """
        Subscribe to a JetStream subject with a durable consumer and process messages asynchronously.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
            durable_name: The durable name for the subscription/consumer. (give a unique name for each consumer)
        """
        try:
            await self.create_stream(topics=[topic])
            consumer_config = ConsumerConfig(
                name=durable_name,
                deliver_policy=DeliverPolicy.ALL,
                durable_name=durable_name,
            )

            await self.js.subscribe(topic, cb=callback, config=consumer_config)
            logging.info(f"Subscribed to async event on topic '{topic}'")

        except Exception as e:
            logging.error(
                f"Failed to subscribe to async event on topic '{topic}': {e}",
                exc_info=True,
            )
            raise e

    async def subscribe_sync_event(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribe to a NATS subject and return a response after processing the message.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
        """
        try:
            await self.nc.subscribe(topic, cb=callback)
            logging.info(f"Subscribed to sync event on topic '{topic}'")

        except Exception as e:
            logging.error(
                f"Failed to subscribe to sync event on topic '{topic}': {e}",
                exc_info=True,
            )
            raise e
