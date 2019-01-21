from rest_framework import serializers
from .models import Reservation, ReservationMetaData, Cabin


class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = '__all__'


class ReservationItemSerializer(serializers.ModelSerializer):
    cabin = CabinSerializer()

    class Meta:
        model = Reservation
        exclude = ('meta_data', 'id')


class ReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = '__all__'


class PublicReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = ('reservation_items', 'name', 'email')