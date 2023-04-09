"""Модуль описания работы ТС"""
import asyncio
import random
from typing import Any, Coroutine

from connection import Sender


class Vehicle:
    """Класс для описания ТС"""
    def __init__(self, uid: str, number: str, is_online: bool, rent_status: str, options: dict) -> None:
        """
        Инициализация объекта ТС
        :param number: номер ТС
        :param is_online: онлайн статус
        :param rent_status: статус аренды
        :param options: свойства ТС
        """
        self._coro = None  # coroutine
        self._move_coro = None  # moving coroutine
        self._uid = uid
        self._number = number
        self._is_online = is_online
        self._rent_status = rent_status
        self._options = options
        self._distance = 0
        self._prev_speed = 0
        self._speed = 0
        self._sender = Sender('status')
        self._is_moving = False

        self._send_time = 10
        self._send_time_moving = 1

    async def get_info(self) -> dict:
        """Получение информации о ТС"""
        info = {
            'uid': self._uid,
            'data': {
                'number': self._number,
                'is_online': self._is_online,
                'rent_status': self._rent_status,
                'options': self._options,
            }
        }
        return info

    async def get_uid(self) -> str:
        """
        Получение уникального идентификатора ТС

        :return: уникальный идентификатор ТС
        """
        return self._uid

    async def get_coroutine(self) -> Coroutine:
        """
        Получение таски, публикуемой данные

        :return: таска
        """
        return self._coro

    async def set_coroutine(self, coro_id) -> Coroutine:
        """
        Назначение таски, публикуемой данные

        :return: таска
        """
        self._coro = coro_id
        return self._coro

    async def set_online_status(self, new_status: bool) -> bool:
        """
        Изменение статуса онлайн

        :param new_status: новый онлайн статус
        :return: онлайн статус ТС
        """
        self._is_online = new_status
        return self._is_online

    async def get_online_status(self) -> bool:
        """
        Получение онлайн статуса

        :return: онлайн статус ТС
        """
        return self._is_online

    async def set_rent_status(self, new_status: str) -> str | None:
        """
        Изменение статуса аренды

        :param new_status: новый статус аренды
        :return: статус аренды ТС
        """
        self._rent_status = new_status
        return self._rent_status

    async def get_rent_status(self) -> str | None:
        """
        Получение статуса аренды

        :return: статус аренды ТС
        """
        return self._rent_status

    async def set_options(self, new_options: dict) -> bool:
        """
        Обновление всех свойств

        :param new_options: набор новых значений свойств ТС
        :return: получилось обновить свойства или нет
        """
        match new_options:
            case dict():
                self._options = new_options
            case _:
                raise ValueError('Неверное новое значение')
        return True

    async def set_option(self, new_option: dict) -> bool:
        """
        Добавление или изменение свойства

        :param new_option: набор нового значения свойства ТС
        :return: получилось обновить свойство или нет
        """
        match new_option:
            case dict():
                self._options.update(new_option)
            case _:
                raise ValueError('Неверное новое значение')
        return True

    async def get_options(self) -> dict | None:
        """
        Получение свойств

        :return: новые значения свойств
        """
        return self._options

    async def get_option(self, option: int | str) -> Any | None:
        """
        Получение значения свойства по ключу

        :param option: название свойства
        :return: значение свойства
        """
        return self._options.get(option)

    async def set_geos(self, distance, speed) -> None:
        """
        Установка значений геоданных

        :param distance: длина поездки
        :param speed: скорость
        """
        self._distance = distance
        self._speed = speed

    async def get_geos(self) -> dict[str, str | dict[str, int | float]]:
        """
        Получение геоданных

        :return: оставшееся расстояние и текущая скорость
        """
        geo = {
            'uid': self._uid,
            'data': {
                'distance': self._distance,
                'speed': self._speed,
            }
        }
        return geo

    async def start_trip(self, distance, speed) -> None:
        """
        Начало поездки

        :param distance: длина поездки
        :param speed: скорость
        """
        self._is_moving = True
        await self.set_geos(distance, speed)
        if self._move_coro:
            self._move_coro.cancel()
        coro = asyncio.create_task(self.yeild_my_geo())
        self._move_coro = coro

    async def pause_trip(self) -> None:
        """Приостанвока поездки"""
        await self.stop_moving()

    async def finish_trip(self) -> None:
        """Окончание поездки"""
        await self.stop_moving()
        self._move_coro.cancel()
        self._move_coro = None

    async def continue_trip(self) -> None:
        """Продолжение поездки"""
        await self.start_moving()

    async def start_moving(self) -> None:
        """Начало движения"""
        if not self._is_moving:
            self._is_moving = True
            self._prev_speed, self._speed = self._speed, self._prev_speed

    async def stop_moving(self) -> None:
        """Прекращение движения"""
        if self._is_moving:
            self._is_moving = False
            self._prev_speed, self._speed = self._speed, self._prev_speed

    async def move(self) -> None:
        """Имитация движения. Уменьшение расстояния"""
        if self._is_moving:
            self._distance -= self._speed
            if self._distance < 0:
                self._distance = 0
                await self.stop_moving()

    async def yeild_my_info(self) -> None:
        """Метод пушит информацию о ТС"""
        await self._sender.run()
        while True:
            if self._is_online and not self._is_moving:
                msg = await self.get_info()
                await self._sender.send(msg)
                await asyncio.sleep(self._send_time)
            else:
                await asyncio.sleep(0.1)

    async def yeild_my_geo(self) -> None:
        """Метод пушит информацию о ТС во время движения"""
        while True:
            if self._is_online and self._is_moving:
                msg = await self.get_geos()
                await self._sender.send(msg)
                if self._speed > 0:
                    await self.move()
                await asyncio.sleep(self._send_time_moving)

            elif self._is_online and not self._is_moving:
                msg = await self.get_geos()
                await self._sender.send(msg)
                await asyncio.sleep(self._send_time_moving)

    async def exec_command(self, name: str) -> None:
        """
        Имитация выплнения команды

        :param name: название команды
        """
        exec_time = random.randint(1, 15)
        await asyncio.sleep(exec_time)
        info = {
            'uid': self._uid,
            'data': {
                'command': name,
                'time': exec_time
            }
        }
        await self._sender.send(info)
