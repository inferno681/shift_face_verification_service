import json
import logging

from aiokafka import AIOKafkaConsumer  # type: ignore

from app.db import Embedding, get_async_session
from app.service import FaceVerification
from config import config

log = logging.getLogger('uvicorn')


class KafkaConsumer:
    """Kafka consumer."""

    def __init__(self, bootstrap_servers: str):
        """Kafka consumer initialization."""
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None

    def deserializer(self, value):
        """Message deserializer."""
        return json.loads(value)

    async def start(self):
        """Kafka producer start method."""
        self.consumer = AIOKafkaConsumer(
            config.service.kafka_topic,  # type: ignore
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=self.deserializer,
        )
        await self.consumer.start()

    async def stop(self):
        """Kafka producer stop method."""
        if self.consumer:
            await self.consumer.stop()

    async def consume(self, for_test: bool = True):
        """Message reading."""
        cycle = True
        while cycle:
            async for msg in self.consumer:  # type: ignore
                user_id = list(msg.value.keys())[0]
                link = msg.value[user_id]
                result = FaceVerification(
                    user_id=user_id,
                    link=link,
                ).represent()
                log.info(result['embedding'])
                async for session in get_async_session():
                    session.add(
                        Embedding(
                            user_id=int(user_id),
                            link=link,
                            embedding=result['embedding'],
                        ),
                    )
                    await session.commit()
                cycle = for_test


consumer = KafkaConsumer(
    bootstrap_servers=config.service.kafka_url,  # type: ignore
)
