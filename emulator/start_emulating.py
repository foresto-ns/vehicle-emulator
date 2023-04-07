"""Модуль взаимодействия с ТС по MQ"""
import asyncio
import json
import logging
import logging.config
import logging.handlers
import os
from pathlib import Path

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from emulator import Emulator

LOG_DIR = os.path.join(Path(__file__).resolve().parent, 'log')
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

logging.config.fileConfig('logging.conf')


async def on_message(message: AbstractIncomingMessage) -> None:
    """Колбек функция, реагирующая на получение сообщения из MQ"""
    logging.info("Message body is: %r" % message.body)
    msg = json.loads(message.body)
    data = msg.get('data')
    match msg.get('command'):
        case 'create':
            await emul.add_vehicle(**data)

        case 'delete':
            await emul.del_vehicle(data.get('uid'))

        case 'set_options':
            await emul.set_options(data.get('uid'), data.get('options'))

        case 'set_option':
            await emul.set_options(data.get('uid'), data.get('options'))

        case 'set_online_status':
            await emul.set_online(data.get('uid'), data.get('online'))

        case 'set_rent_status':
            await emul.set_rent_status(data.get('uid'), data.get('rent_status'))

        case 'start_trip':
            await emul.start_trip(data.get('uid'), data.get('distance'), data.get('speed'))

        case 'pause_trip':
            await emul.pause_trip(data.get('uid'))

        case 'continue_trip':
            await emul.continue_trip(data.get('uid'))

        case 'finish_trip':
            await emul.finish_trip(data.get('uid'))

        case 'exec_command':
            await emul.exec_command(data.get('uid'), data.get('name'))


async def main():
    """Запуск имитации работы ТС"""

    login = os.environ['RM_USER']
    password = os.environ['RM_PASSWORD']
    host = os.environ['RM_HOST']
    connection = await connect(f'amqp://{login}:{password}@{host}/')
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("commands")
        await queue.consume(on_message, no_ack=True)
        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == '__main__':
    emul = Emulator()
    asyncio.run(main())
