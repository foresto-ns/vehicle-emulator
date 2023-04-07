from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from api.models import Vehicle, Command


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'rent_status', 'is_online', 'options', 'create_date')
    list_filter = ('rent_status', 'is_online', 'create_date')
    ordering = ('-create_date',)
    search_fields = ('number', 'options')


@admin.register(Command)
class CommandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'execution_time', 'vehicle')
    list_filter = ('name', 'execution_time', 'vehicle')
    ordering = ('-create_date',)
    search_fields = ('name', 'vehicle')
