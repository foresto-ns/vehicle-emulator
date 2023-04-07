from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.viewsets import GenericViewSet

from api import serializers
from api.models import Vehicle, Command, Trip
from api.utils import send_msg_to_mq


class VehicleViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """Управление ТС"""
    queryset = Vehicle.objects.all()
    serializer_class = serializers.VehicleSerializer
    filter_backends = {DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter}
    filterset_fields = ['create_date', 'id', 'is_online', 'number', 'rent_status']
    search_fields = ['is_online', 'number', 'options', 'rent_status']
    ordering_fields = ['number', 'create_date']
    ordering = ['number']
    swagger_tags = ['vehicle']

    def perform_create(self, serializer):
        serializer.save()
        number = serializer.data.get('number')
        is_online = serializer.data.get('is_online')
        rent_status = serializer.data.get('rent_status')
        options = serializer.data.get('options')
        vehicle = str(serializer.data.get('id'))
        msg = {
            'command': 'create',
            'data': {
                'uid': vehicle,
                'number': number,
                'is_online': is_online,
                'rent_status': rent_status,
                'options': options
            }
        }
        send_msg_to_mq(msg)

    def perform_destroy(self, instance):
        msg = {
            'command': 'delete',
            'data': {
                'uid': str(instance.id)
            }
        }
        send_msg_to_mq(msg)
        instance.delete()


class CommandViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """Управление командами"""
    queryset = Command.objects.all()
    serializer_class = serializers.CommandSerializer
    filter_backends = {DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter}
    filterset_fields = ['name', 'id', 'execution_time', 'vehicle', 'create_date']
    search_fields = ['name', 'id', 'execution_time', 'vehicle']
    ordering_fields = ['create_date', 'name']
    ordering = ['create_date', 'name']
    swagger_tags = ['commands']

    def perform_create(self, serializer):
        serializer.save()
        name = serializer.data.get('name')
        vehicle = str(serializer.data.get('vehicle'))
        msg = {
            'command': 'exec_command',
            'data': {
                'uid': vehicle,
                'name': name
            }
        }
        send_msg_to_mq(msg)


class TripViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Управление поездками"""
    queryset = Trip.objects.all()
    filter_backends = {DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter}
    filterset_fields = ['id', 'point_from', 'point_to', 'distance', 'speed', 'start_date', 'is_done', 'vehicle']
    search_fields = ['id', 'point_from', 'point_to', 'distance', 'speed', 'start_date', 'is_done', 'vehicle']
    ordering_fields = ['start_date', 'distance', 'speed']
    ordering = ['create_date']
    swagger_tags = ['trip']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.TripCreateSerializer
        return serializers.TripGetSerializer

    def perform_create(self, serializer):
        serializer.save()
        distance = serializer.data.get('distance')
        speed = serializer.data.get('speed')
        vehicle = str(serializer.data.get('vehicle'))
        msg = {
            'command': 'start_trip',
            'data': {
                'uid': vehicle,
                'distance': distance,
                'speed': speed
            }
        }
        send_msg_to_mq(msg)
