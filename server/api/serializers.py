"""Описание сериализаторов модуля api"""
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from api.models import Vehicle, Command, Trip


class VehicleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Vehicle"""
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleOptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели Vehicle. Работает со свойствами ТС"""
    def update(self, instance, validated_data):
        option = {k: v for k, v in validated_data}
        instance.options.update(option)

    class Meta:
        model = Vehicle
        fields = 'options'


class CommandSerializer(serializers.ModelSerializer):
    """Сериализатор модели Command"""
    def validate(self, attrs):
        if 'no_validate' not in attrs or attrs['no_validate'] is False:
            vehicle = Vehicle.objects.get(id=attrs.get('vehicle').id)
            if vehicle.is_online is False:
                raise ValidationError(
                    detail={'error': 'Транспортное средство оффлайн. Вы не можете отправить команду'},
                    code=status.HTTP_400_BAD_REQUEST
                )
        return attrs

    class Meta:
        model = Command
        fields = '__all__'


class TripCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Trip для создания или изменения данных"""
    def validate(self, attrs):
        if 'no_validate' not in attrs or attrs['no_validate'] is False:
            vehicle = Vehicle.objects.get(id=attrs.get('vehicle').id)
            not_finished_trip = Trip.objects.filter(is_done=False).exists()
            if not vehicle.is_online:
                raise ValidationError(
                    detail={'error': 'Транспортное средство оффлайн. Вы не можете начать поездку'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            if not_finished_trip and self.context.get('request').method == 'POST':
                raise ValidationError(
                    detail={'error': 'Транспортное средство находится в поездке. Вы не можете начать еще одну поездку'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            if vehicle.rent_status != 'On_lease':
                raise ValidationError(
                    detail={'error': 'Транспортное средство не находится в аренде. Вы не можете начать поездку'},
                    code=status.HTTP_400_BAD_REQUEST
                )
        return attrs

    class Meta:
        model = Trip
        fields = '__all__'


class TripGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели Trip для получения данных"""
    class Meta:
        model = Trip
        fields = '__all__'


class SetOnlineSerializer(serializers.Serializer):
    """Сериализатор статуса онлайн ТС"""
    online = serializers.BooleanField()


class SetRentStatusSerializer(serializers.Serializer):
    """Сериализатор статуса аренды ТС"""
    rent_status = serializers.CharField(max_length=32)


class OptionsSerializer(serializers.Serializer):
    """Сериализатор свойств ТС"""
    key = serializers.Field()


class ErrorSerializer(serializers.Serializer):
    """Дефолтный сериализатор с ошибкой"""
    error = serializers.CharField(read_only=True)
