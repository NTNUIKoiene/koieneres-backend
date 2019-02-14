from rest_framework import serializers
from .models import Reservation, ReservationMetaData, Cabin
from utils.dateutils import daterange
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.db import transaction
from utils.validators import validate_selected_dates
from utils.dateutils import string_to_date


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
            data[str(
                reservation['date']
            )]['booked'] += reservation['members'] + reservation['non_members']
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

    def create(self, validated_data):
        try:
            with transaction.atomic():
                metadata = super().create(validated_data)
                user = self.context['request'].user
                metadata.created_by = user
                metadata.save()
                if not metadata.should_pay:
                    assert user.is_cabin_board, 'Only cabin board members can reserve free cabins'
                selected_dates = self.initial_data['selected_dates']
                assert validate_selected_dates(
                    selected_dates,
                    user.is_cabin_board), 'Selected dates are invalid'
                # TODO: Validate reservation period
                # TODO: Validate is closed
                # Create reservations
                total_price = 0
                for selected_date in selected_dates:
                    cabin = Cabin.objects.get(name=selected_date['name'])
                    date = string_to_date(selected_date['date_key'])
                    total_price += selected_date['members'] * cabin.member_price
                    total_price += selected_date['non_members'] * cabin.non_member_price
                    reservation = Reservation(
                        cabin=cabin,
                        date=date,
                        members=selected_date['members'],
                        non_members=selected_date['non_members'],
                        meta_data=metadata)
                    reservation.save()
                metadata.total_price = total_price
                metadata.save()
                return metadata
        except AssertionError as e:
            raise serializers.ValidationError(e)


class PublicReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = ('reservation_items', 'name', 'email')