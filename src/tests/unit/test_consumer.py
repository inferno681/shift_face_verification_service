import logging
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.anyio
async def test_consumer(consumer_test_data, caplog):
    """Kafka consumer test."""
    from app.service import consumer

    caplog.set_level(logging.INFO)
    mock_msg = MagicMock()
    mock_msg.value = consumer_test_data
    consumer.consumer = AsyncMock()
    consumer.consumer.__aiter__.return_value = [mock_msg]
    await consumer.consume(for_test=False)
    record = caplog.records[0]
    assert record.levelname == 'INFO'
    assert len(record.message.strip('][').split(', ')) == 128
