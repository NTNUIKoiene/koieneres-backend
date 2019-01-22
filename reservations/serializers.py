from rest_framework import serializers
from .models import Reservation, ReservationMetaData, Cabin
from utils.dateutils import daterange
from django.db.models import Sum, F
from django.db.models.functions import Coalesce


class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = '__all__'


class CabinStatusSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        """
        Uses the context from request (containing a date range) to aggregate
        bookings for the cabin.
        """
        from_date = self.context['from']
        to_date = self.context['to']
        reservations = Reservation.objects.select_related('cabin').filter(
            date__gte=from_date, date__lte=to_date)
        print(from_date, to_date)
        data = {}
        for date in daterange(from_date, to_date):
            result = reservations.filter(date=date).aggregate(
                booked=Coalesce(Sum(F('members') + F('non_members')), 0))
            # TODO: Check if cabin is closed
            is_closed = False
            result['isClosed'] = is_closed
            data[str(date)] = result
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
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = '__all__'


class PublicReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = ('reservation_items', 'name', 'email')