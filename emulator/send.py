import asyncio
import json
import time

from connection import Sender

# CREATE_MSG = {
#         'command': 'create',
#         'data': {
#             'uid': '0b9fa607-63be-48b6-a9e6-d47d3a9f0a97',
#             'number': 'a001a778',
#             'is_online': True,
#             'rent_status': 'Not_available',
#             'options': {
#                 "color": "Black"
#             }
#         }
#     }

# DELETE_MSG = {
#     'command': 'delete',
#     'data': {
#         'uid': '123'
#     }
# }

# SET_OPTIONS = {
#     'command': 'set_options',
#     'data': {
#         'uid': '123',
#         'options': {'color': 'white'}
#     }
# }

# SET_ONLINE = {
#     'command': 'set_online_status',
#     'data': {
#         'uid': '123',
#         'online': True
#     }
# }
#
# SET_RENT_STATUS = {
#     'command': 'set_rent_status',
#     'data': {
#         'uid': '123',
#         'rent_status': 'Pause'
#     }
# }

# START_TRIP = {
#     'command': 'start_trip',
#     'data': {
#         'uid': '123',
#         'distance': 12,
#         'speed': 0.25
#     }
# }
#
# PAUSE_TRIP = {
#     'command': 'pause_trip',
#     'data': {
#         'uid': '123',
#     }
# }
#
# CONTINUE_TRIP = {
#     'command': 'continue_trip',
#     'data': {
#         'uid': '123',
#     }
# }
#
# FINISH_TRIP = {
#     'command': 'finish_trip',
#     'data': {
#         'uid': '123',
#     }
# }
#
# COMMAND = {
#     'command': 'exec_command',
#     'data': {
#         'uid': '123',
#         'name': 'asdasd'
#     }
# }


import pika

credentials = pika.PlainCredentials(**{'username': 'rmuser', 'password': 'rmpassword'})
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='commands')


channel.basic_publish(exchange='', routing_key='commands', body=json.dumps(CREATE_MSG).encode('ascii'))
# time.sleep(10)
# channel.basic_publish(exchange='', routing_key='commands', body=json.dumps(DELETE_MSG).encode('ascii'))


if __name__ == '__main__':
    connection.close()


# async def main():
#     conn = Sender('test')
#     await conn.run()
#
#     await conn.send(CREATE_MSG)
#     await asyncio.sleep(5)
#     await conn.send(START_TRIP)
#     await asyncio.sleep(5)
#     # await conn.send(PAUSE_TRIP)
#     # await asyncio.sleep(10)
#     # await conn.send(CONTINUE_TRIP)
#     # await asyncio.sleep(5)
#     await conn.send(FINISH_TRIP)
#     await asyncio.sleep(5)
#     # await conn.send(SET_RENT_STATUS)
#     # await asyncio.sleep(20)
#     await conn.send(DELETE_MSG)
#     # await conn.send(COMMAND)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
