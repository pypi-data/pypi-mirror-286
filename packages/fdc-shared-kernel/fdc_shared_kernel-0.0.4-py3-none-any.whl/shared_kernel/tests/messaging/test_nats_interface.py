import asyncio
from unittest.mock import patch
from nats.aio.client import Client as NATS
import pytest


@pytest.mark.asyncio
async def test_nats_subscriber():
    # Start the patch
    mock_client = patch('nats.aio.client.Client').start()

    # Get the mock instance
    instance = mock_client.return_value

    # Configure the mock to return True for is_connected and None for publish
    instance.is_connected.return_value = True
    instance.publish.return_value = None

    try:
        # Initialize the NATS client
        nc = NATS()

        # Connect to the mock NATS server
        await nc.connect('nats://localhost:4222')

        # Subscribe to a topic asynchronously
        await nc.subscribe('foo', cb=lambda m: print(f'Received: {m.data}'))

        # Publish a message to the subscribed topic
        await nc.publish('foo', b'bar')

        # Assert that the callback was called with the published message
        instance.publish.assert_called_once_with('foo', b'bar')
    finally:
        # Stop the patch after the test
        mock_client.stop()
