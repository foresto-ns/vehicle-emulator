"""Описание работы эмулятора"""
import asyncio

from vehicle import Vehicle


class Emulator:
    def __init__(self):
        self.garage = {}

    async def add_vehicle(self, uid: str, number: str, is_online: bool, rent_status: str, options: dict) -> None:
        """Создание ТС с присваиванием ему таски"""
        vehicle = Vehicle(uid, number, is_online, rent_status, options)

        coro = asyncio.create_task(vehicle.yeild_my_info())
        await vehicle.set_coroutine(coro)

        self.garage[uid] = vehicle

    async def del_vehicle(self, uid: str) -> None:
        """Удаление ТС"""
        vehicle = self.garage.pop(uid)
        coro = await vehicle.get_coroutine()
        coro.cancel()
        await asyncio.sleep(0.1)

    async def set_options(self, uid: str, options: dict) -> None:
        """
        Установка свойств у ТС
        :param uid: уникальный идентификатор ТС
        :param options: свойства
        """
        await self.garage[uid].set_options(options)

    async def set_option(self, uid: str, option: dict) -> None:
        """
        Установка свойства у ТС
        :param uid: уникальный идентификатор ТС
        :param option: свойство
        """
        await self.garage[uid].set_option(option)

    async def set_online(self, uid: str, online: bool) -> None:
        """
        Установка онлайн статуса у ТС
        :param uid: уникальный идентификатор ТС
        :param online: новое значение статуса
        """
        await self.garage[uid].set_online_status(online)

    async def set_rent_status(self, uid: str, status: str) -> None:
        """
        Установка статуса аренды у ТС
        :param uid: уникальный идентификатор ТС
        :param status: новое значение статуса
        """
        await self.garage[uid].set_rent_status(status)

    async def start_trip(self, uid: str, distance: float, speed: float) -> None:
        """
        Старт поездки
        :param uid: уникальный идентификатор ТС
        :param distance: длина поездки
        :param speed: скорость
        """
        await self.garage[uid].start_trip(distance, speed)

    async def pause_trip(self, uid: str) -> None:
        """
        Приостановка поездки
        :param uid: уникальный идентификатор ТС
        """
        await self.garage[uid].pause_trip()

    async def continue_trip(self, uid: str) -> None:
        """
        Продолжение поездки
        :param uid: уникальный идентификатор ТС
        """
        await self.garage[uid].continue_trip()

    async def finish_trip(self, uid: str) -> None:
        """
        Окончание поездки
        :param uid: уникальный идентификатор ТС
        """
        await self.garage[uid].finish_trip()

    async def exec_command(self, uid: str, name: str) -> None:
        """
        Запуск начала обработки команды
        :param uid: уникальный идентификатор ТС
        :param name: название команды
        """
        await self.garage[uid].exec_command(name)
