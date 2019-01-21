from rest_framework import serializers
from .models import Reservation, ReservationMetaData, Cabin


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class ReservationMetaDataSerializer(serializers.ModelSerializer):
    class ReservationItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = Reservation
            exclude = ('meta_data', 'id')

    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = '__all__'