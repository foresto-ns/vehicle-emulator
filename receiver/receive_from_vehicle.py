"""Модуль прослушки сообщений, отправляемых ТС"""
import os
import asyncio
import logging
import logging.config
import logging.handlers
from pathlib import Path

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

LOG_DIR = os.path.join(Path(__file__).resolve().parent, 'log')
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

logging.config.fileConfig('logging.conf')


async def on_message(message: AbstractIncomingMessage) -> None:
    """Колбек функция, реагирующая на получение сообщения из MQ"""
    # print(" [x] Received message %r" % message)
    logging.info("Message body is: %r" % message.body)


async def main():
    """Запуск прослушки сообщений от ТС"""
    login = os.environ['RM_USER']
    password = os.environ['RM_PASSWORD']
    host = os.environ['RM_HOST']
    connection = await connect(f'amqp://{login}:{password}@{host}/')
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("status")
        await queue.consume(on_message, no_ack=True)
        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
