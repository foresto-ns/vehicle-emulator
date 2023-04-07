"""Описание вспомогательных методов модуля"""
import json
import logging

import pika

from server.settings import env

logger = logging.getLogger(__name__)


def send_msg_to_mq(message: dict):
    """Отправка команды в MQ"""
    logger.info(message)
    credentials = pika.PlainCredentials(username=env("RM_USER"), password=env("RM_PASSWORD"))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=env("RM_HOST"), credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='commands')

    channel.basic_publish(exchange='', routing_key='commands', body=json.dumps(message).encode('ascii'))

    connection.close()
