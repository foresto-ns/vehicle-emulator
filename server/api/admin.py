from django.contrib import admin

from api.models import Vehicle, Command, Trip


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'rent_status', 'is_online', 'options', 'create_date')
    list_filter = ('rent_status', 'is_online', 'create_date')
    ordering = ('-create_date',)
    search_fields = ('number', 'options')


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'execution_time', 'vehicle')
    list_filter = ('name', 'execution_time', 'vehicle')
    ordering = ('-create_date',)
    search_fields = ('name', 'vehicle')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('point_from', 'point_to', 'is_done', 'distance', 'speed', 'vehicle', 'start_date')
    list_filter = ('is_done', 'vehicle')
    ordering = ('-start_date',)
    search_fields = ('point_from', 'point_to', 'distance', 'speed', 'vehicle')
