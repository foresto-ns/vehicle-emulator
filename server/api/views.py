from django.http import Http404
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Vehicle, Trip
from api.serializers import VehicleSerializer, SetOnlineSerializer, SetRentStatusSerializer, OptionsSerializer, \
    ErrorSerializer
from api.utils import send_msg_to_mq


def index(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'api/index.html', context)


def show_vehicle_info(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    context = {
        'vehicle': vehicle
    }
    return render(request, 'api/detail.html', context)


class VehicleOptions(APIView):
    """Управление свойствами ТС"""
    swagger_tags = ['options']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    options_response = openapi.Response('Все свойства у ТС', OptionsSerializer)
    error_response = openapi.Response('Транспортное средство оффлайн', ErrorSerializer)
    empty_response = openapi.Response('Свойства удалены', None)

    @swagger_auto_schema(responses={200: options_response, 400: error_response})
    def get(self, request, pk, format=None):
        """Получение значений свойств ТС"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете получить свойства ТС'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = VehicleSerializer(snippet)
        return Response(serializer.data.get('options'))

    @swagger_auto_schema(responses={200: options_response, 400: error_response})
    def patch(self, request, pk, format=None):
        """Обновление и добавление значений свойств ТС"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете поменять свойства ТС'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data:
            snippet.options.update(request.data)
            snippet.save()
            msg = {
                'command': 'set_options',
                'data': {
                    'uid': pk,
                    'options': request.data
                }
            }
            send_msg_to_mq(msg)
        return Response(VehicleSerializer(snippet).data.get('options'))

    @swagger_auto_schema(responses={204: empty_response, 400: error_response})
    def delete(self, request, pk, format=None):
        """Удаление всех свойств у ТС"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете удалить свойства ТС'},
                status=status.HTTP_400_BAD_REQUEST
            )
        snippet.options = {}
        snippet.save()
        msg = {
            'command': 'set_options',
            'data': {
                'uid': pk,
                'options': {}
            }
        }
        send_msg_to_mq(msg)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FinishTrip(APIView):
    """Завершение поездки"""
    swagger_tags = ['trip']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    finish_response = openapi.Response('Поездка завершена', None)
    error_response = openapi.Response('Транспортное средство оффлайн или нет незавершенной поездки', ErrorSerializer)

    @swagger_auto_schema(responses={200: finish_response, 400: error_response})
    def get(self, request, pk, format=None):
        """Завершение поездки"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете завершить поездку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip = Trip.objects.get(vehicle=pk, is_done=False)
        if not trip:
            return Response({'error': 'Незавершенной поездки нет'}, status=status.HTTP_400_BAD_REQUEST)
        msg = {
            'command': 'finish_trip',
            'data': {
                'uid': str(trip.vehicle.id),
            }
        }
        send_msg_to_mq(msg)
        trip.is_done = True
        trip.save()
        return Response(status=status.HTTP_200_OK)


class ContinueTrip(APIView):
    """Продолжение поездки"""
    swagger_tags = ['trip']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    continue_response = openapi.Response('Поездка возобновлена', None)
    error_response = openapi.Response('Транспортное средство оффлайн или нет незавершенной поездки', ErrorSerializer)

    @swagger_auto_schema(responses={200: continue_response, 400: error_response})
    def get(self, request, pk, format=None):
        """Продолжение поездки"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете продолжить поездку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip = Trip.objects.filter(vehicle=pk, is_done=False)
        if not trip.exists():
            return Response({'error': 'Незавершенной поездки нет'}, status=status.HTTP_400_BAD_REQUEST)
        msg = {
            'command': 'continue_trip',
            'data': {
                'uid': trip.vehicle,
            }
        }
        send_msg_to_mq(msg)
        return Response(status=status.HTTP_200_OK)


class PauseTrip(APIView):
    """Приостановка поездки"""
    swagger_tags = ['trip']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    pause_response = openapi.Response('Поездка приостановлена', None)
    error_response = openapi.Response('Транспортное средство оффлайн или нет незавершенной поездки', ErrorSerializer)

    @swagger_auto_schema(responses={200: pause_response, 400: error_response})
    def get(self, request, pk, format=None):
        """Приостановка поездки"""
        snippet = self.get_object(pk)
        if snippet.is_online is False:
            return Response(
                {'error': 'Транспортное средство оффлайн. Вы не можете приостановить поездку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip = Trip.objects.filter(vehicle=pk, is_done=False)
        if not trip.exists():
            return Response({'error': 'Незавершенной поездки нет'}, status=status.HTTP_400_BAD_REQUEST)
        msg = {
            'command': 'pause_trip',
            'data': {
                'uid': trip.vehicle,
            }
        }
        send_msg_to_mq(msg)
        return Response(status=status.HTTP_200_OK)


class SetOnlineStatus(APIView):
    """Изменение статуса online"""
    swagger_tags = ['vehicle']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    pause_response = openapi.Response('Статус изменен', VehicleSerializer)
    error_response = openapi.Response('Невалидные данные', ErrorSerializer)

    @swagger_auto_schema(responses={200: pause_response, 400: error_response})
    def patch(self, request, pk, format=None):
        """Изменение статуса online"""
        snippet = self.get_object(pk)
        serializer = SetOnlineSerializer(data=request.data)
        if serializer.is_valid():
            st = serializer.data.get('online')
            snippet.is_online = st
            snippet.save()
            msg = {
                'command': 'set_online_status',
                'data': {
                    'uid': pk,
                    'online': st
                }
            }
            send_msg_to_mq(msg)
            return Response(VehicleSerializer(snippet).data)


class SetRentStatus(APIView):
    """Изменение статуса аренды"""
    swagger_tags = ['vehicle']

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    pause_response = openapi.Response('Статус изменен', VehicleSerializer)
    error_response = openapi.Response('Невалидные данные или транспортное средство оффлайн', ErrorSerializer)

    @swagger_auto_schema(responses={200: pause_response, 400: error_response})
    def patch(self, request, pk, format=None):
        """Изменение статуса аренды"""
        snippet = self.get_object(pk)
        serializer = SetRentStatusSerializer(data=request.data)
        if serializer.is_valid():
            if snippet.is_online is False:
                return Response(
                    {'error': 'Транспортное средство оффлайн. Вы не можете поменять статус аренды'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            st = serializer.data.get('rent_status')
            snippet.rent_status = st
            snippet.save()
            msg = {
                'command': 'set_rent_status',
                'data': {
                    'uid': pk,
                    'rent_status': st
                }
            }
            send_msg_to_mq(msg)
            return Response(VehicleSerializer(snippet).data)
