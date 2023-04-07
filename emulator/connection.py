"""Описание коннектора MQ"""
import json
import os

from aio_pika import connect, Message


class MQConnection:
    def __init__(self, queue: str):
        self.__login = os.environ['RM_USER']
        self.__password = os.environ['RM_PASSWORD']
        self.__host = os.environ['RM_HOST']
        self._queue = None
        self._queue_name = queue
        self._url = f'amqp://{self.__login}:{self.__password}@{self.__host}/'
        self._channel = None
        self._connection = None

    async def run(self):
        """Запуск коннектора"""
        self._connection = await connect(self._url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._queue_name)


class Sender(MQConnection):
    async def send(self, message):
        """Отправка сообщения в MQ"""
        await self._channel.default_exchange.publish(
            Message(json.dumps(message).encode('ascii')),
            routing_key=self._queue.name,
        )
