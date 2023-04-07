"""Описание моделей данных модуля api"""
import random
import uuid

from django.db import models
from django.urls import reverse


def get_random_distance():
    return random.randint(0, 100)


class Vehicle(models.Model):
    """Модель ТС"""
    rent_choice = [
        ('Available', 'Доступен для аренды'),
        ('Not_available', 'Не доступен для аренды'),
        ('On_lease', 'В аренде'),
        ('Pause', 'Пауза'),
        ('Maintenance', 'На обслуживании')
    ]

    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, verbose_name='Уникальный ключ в системе')
    number = models.CharField(unique=True, max_length=32, verbose_name='Номер ТС')
    rent_status = models.CharField(
        max_length=32,
        verbose_name='Текущий статус аренды ТС',
        default='Not_available',
        choices=rent_choice
    )
    is_online = models.BooleanField(verbose_name='Устройство online?', default=False)
    options = models.JSONField(verbose_name='Свойства ТС', default=dict, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания ТС')

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def get_absolute_url(self):
        return reverse('vehicle_info', kwargs={'pk': self.id})


class Command(models.Model):
    """Модель команд"""
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False, verbose_name='Уникальный ключ в системе')
    name = models.CharField(max_length=64, verbose_name='Название команды')
    execution_time = models.FloatField(null=True, verbose_name='Время выполнения программы в секундах', editable=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, verbose_name='Транспортное средство')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки команды')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class Trip(models.Model):
    """Модель поездок"""
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False,
                          verbose_name='Уникальный ключ в системе')
    point_from = models.CharField(max_length=64, verbose_name='Место отправления')
    point_to = models.CharField(max_length=64, verbose_name='Место назначения')
    distance = models.IntegerField(verbose_name='Расстояние', default=get_random_distance)
    speed = models.FloatField(verbose_name='Скорость')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Время начала поездки')
    is_done = models.BooleanField(default=False, verbose_name='Поездка закончилась')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='Транспортное средство')

    class Meta:
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"
