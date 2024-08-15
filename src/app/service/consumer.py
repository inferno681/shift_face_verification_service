import json
import logging

from aiokafka import AIOKafkaConsumer  # type: ignore

from app.service import FaceVerification
from config import config

log = logging.getLogger('uvicorn')


class KafkaConsumer:
    """Класс консьюмера кафка для удобства инициализации."""

    def __init__(self, bootstrap_servers: str):
        """Конструктор класса."""
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None

    def deserializer(self, value):
        """Метод десериализации сообщений."""
        return json.loads(value)

    async def start(self):
        """Метод запуска консьюмера в одном event_loop с приложением."""
        self.consumer = AIOKafkaConsumer(
            'faces',
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=self.deserializer,
        )
        await self.consumer.start()

    async def stop(self):
        """Метод остановки консьюмера."""
        if self.consumer:
            await self.consumer.stop()

    async def consume(self):
        """Чтение сообщений из кафка."""
        while True:
            async for msg in self.consumer:
                user_id = list(msg.value.keys())[0]
                link = msg.value[user_id]
                result = FaceVerification(
                    user_id=user_id,
                    link=link,
                ).represent()
                log.info(result['embedding'])

    async def check(self):
        """Метод для проверки доступности кафка."""
        try:
            await self.start()
            await self.stop()
        except Exception:
            return False
        return True


consumer = KafkaConsumer(
    bootstrap_servers=config.service.kafka_url(),  # type: ignore
)
