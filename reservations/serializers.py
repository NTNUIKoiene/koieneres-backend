from rest_framework import serializers
from .models import Reservation, ReservationMetaData, Cabin
from utils.dateutils import daterange
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.db import transaction


class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        """
        Uses the context from request (containing a date range) to aggregate
        bookings for the cabin.
        """
        from_date = self.context['from']
        to_date = self.context['to']
        data = {}
        for date in daterange(from_date, to_date):
            data[str(date)] = {'is_closed': False, 'booked': 0}
        reservations = Reservation.objects.filter(
            date__gte=from_date, date__lte=to_date, cabin=instance).values(
                'members', 'non_members', 'date')
        for reservation in reservations:
            data[str(reservation['date']
                     )] = reservation['members'] + reservation['non_members']

        return data

    class Meta:
        model = Cabin
        fields = '__all__'


class ReservationItemSerializer(serializers.ModelSerializer):
    cabin = CabinSerializer()

    class Meta:
        model = Reservation
        exclude = ('meta_data', 'id')


class ReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(), many=True)

    class Meta:
        model = ReservationMetaData
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            metadata = super().create(validated_data)
            metadata.created_by = self.context['request'].user
            metadata.save()
            assert False
            return metadata


class PublicReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = ('reservation_items', 'name', 'email')