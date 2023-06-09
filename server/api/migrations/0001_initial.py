# Generated by Django 4.1.7 on 2023-04-02 22:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный ключ в системе')),
                ('number', models.CharField(max_length=32, unique=True, verbose_name='Номер ТС')),
                ('rent_status', models.CharField(choices=[('Available', 'Доступен для аренды'), ('Not_available', 'Не доступен для аренды'), ('On_lease', 'В аренде'), ('Pause', 'Пауза'), ('Maintenance', 'На обслуживании')], default='Not_available', max_length=32, verbose_name='Текущий статус аренды ТС')),
                ('is_online', models.BooleanField(default=False, verbose_name='Устройство online?')),
                ('options', models.JSONField(blank=True, default=dict, verbose_name='Свойства ТС')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания ТС')),
            ],
            options={
                'verbose_name': 'Транспортное средство',
                'verbose_name_plural': 'Транспортные средства',
            },
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный ключ в системе')),
                ('name', models.CharField(max_length=64, verbose_name='Название команды')),
                ('execution_time', models.FloatField(blank=True, null=True, verbose_name='Время выполнения программы в секундах')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки команды')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.vehicle', verbose_name='Транспортное средство')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
    ]
