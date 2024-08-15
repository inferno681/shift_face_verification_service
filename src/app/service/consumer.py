import json

from aiokafka import AIOKafkaConsumer  # type: ignore

from config import config


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
            data = await self.consumer.getmany()
            for tp, messages in data.items():
                for message in messages:
                    print(type(message.value), message.value)

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
