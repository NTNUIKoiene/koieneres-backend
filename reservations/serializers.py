from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from utils.dateutils import daterange, string_to_date
from utils.validators import validate_selected_dates

from .models import (
    Cabin,
    CabinClosing,
    ExtendedPeriod,
    Reservation,
    ReservationMetaData,
)


class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = "__all__"


class ExtendedPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedPeriod
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_cabin_board:
            raise PermissionDenied()
        if not validated_data["reservation_date"] < validated_data["end_date"]:
            raise serializers.ValidationError(
                "Reservation date must be before end date"
            )
        if not validated_data["reservation_date"].weekday() == 2:
            raise serializers.ValidationError("Reservation date must be a wednesday")
        if not validated_data["end_date"].weekday() == 3:
            raise serializers.ValidationError("End date must be a thursday")
        return super().create(validated_data)


class CabinClosingListSerializer(serializers.ModelSerializer):
    cabin = CabinSerializer(many=False, read_only=True)

    class Meta:
        model = CabinClosing
        exclude = ("created_by",)


class CabinClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinClosing
        exclude = ("created_by",)

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_cabin_board:
            raise PermissionDenied()
        if not validated_data["from_date"] < validated_data["to_date"]:
            raise serializers.ValidationError("From date must be before to date.")
        closing = super().create(validated_data)
        closing.created_by = user
        closing.save()
        return closing


class StatusSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        """
        Uses the context from request (containing a date range) to aggregate
        bookings for the cabin.
        """
        from_date = self.context["from"]
        to_date = self.context["to"]
        data = {}
        for date in daterange(from_date, to_date):
            data[str(date)] = {"is_closed": False, "booked": 0}
        closings = CabinClosing.objects.filter(cabin=instance, from_date__gte=from_date)
        for closing in closings:
            for date in daterange(closing.from_date, min(closing.to_date, to_date)):
                data[str(date)]["is_closed"] = True
        reservations = Reservation.objects.filter(
            date__gte=from_date, date__lte=to_date, cabin=instance
        ).values("members", "non_members", "date")
        for reservation in reservations:
            data[str(reservation["date"])]["booked"] += (
                reservation["members"] + reservation["non_members"]
            )
        return data

    class Meta:
        model = Cabin
        fields = "__all__"


class ReservationItemSerializer(serializers.ModelSerializer):
    cabin = CabinSerializer()

    class Meta:
        model = Reservation
        exclude = ("meta_data", "id")


class ReservationMetaDataSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReservationMetaData
        fields = "__all__"

    def create(self, validated_data):
        try:
            with transaction.atomic():
                metadata = super().create(validated_data)
                user = self.context["request"].user
                metadata.created_by = user
                metadata.save()
                if not metadata.should_pay:
                    assert (
                        user.is_cabin_board
                    ), "Only cabin board members can reserve free cabins"
                selected_dates = self.initial_data["selected_dates"]
                assert validate_selected_dates(
                    selected_dates, user.is_cabin_board
                ), "Selected dates are invalid"
                # TODO: Validate reservation period
                # TODO: Validate is closed
                # Create reservations
                total_price = 0
                for selected_date in selected_dates:
                    cabin = Cabin.objects.get(name=selected_date["name"])
                    date = string_to_date(selected_date["date_key"])
                    total_price += selected_date["members"] * cabin.member_price
                    total_price += selected_date["non_members"] * cabin.non_member_price
                    reservation = Reservation(
                        cabin=cabin,
                        date=date,
                        members=selected_date["members"],
                        non_members=selected_date["non_members"],
                        meta_data=metadata,
                    )
                    reservation.save()
                metadata.total_price = total_price
                metadata.save()
                return metadata
        except AssertionError as e:
            raise serializers.ValidationError(e)

    def update(self, instance, validated_data):
        instance.membership_number = validated_data.get(
            "membership_number", instance.membership_number
        )
        instance.name = validated_data.get("name", instance.name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        user = self.context["request"].user
        if not validated_data.get("should_pay", True) and not user.is_cabin_board:
            raise serializers.ValidationError(
                "must be cabin board to mark reservation as free"
            )
        instance.should_pay = validated_data.get("should_pay", instance.should_pay)
        instance.is_paid = validated_data.get("is_paid", instance.is_paid)
        instance.save()
        return instance

